// API client for Concept MRI backend
import type {
  SessionStatus,
  SessionListItem,
  SessionDetailResponse,
  TrajectoryPointsResponse,
  ClusteringSchema,
  SentenceExperimentRequest,
  SentenceExperimentResponse,
} from '../types/api';
import type {
  Fingerprint, JobView, LensBuildBody, LensDetail, LensFlows, LensMembersPage, LensMethods, LensOptions, LensSearch,
  LensSummary, LensMarks, LensNodeDetails, LensVersion, MassMeanDetails, MassMeanValidation, MembersQuery, Population,
  TuneBody, Validation,
} from '../types/lens';
import type { AnalystTests, Card, QuestionAnswer } from '../types/cards';

export const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Error class for API-related errors
 */
export class ApiError extends Error {
  status: number
  response?: unknown

  constructor(message: string, status: number, response?: unknown) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.response = response;
  }
}

/**
 * API client for Concept MRI backend
 */
class ConceptMriApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}, timeoutMs = 300000): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
      signal: controller.signal,
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        let errorResponse;
        
        try {
          errorResponse = await response.json();
          errorMessage = errorResponse.detail || errorMessage;
        } catch {
          // If response isn't JSON, use status text
          errorMessage = response.statusText || errorMessage;
        }

        throw new ApiError(errorMessage, response.status, errorResponse);
      }

      return response.json();
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      if (error instanceof DOMException && error.name === 'AbortError') {
        throw new ApiError('Request timed out — server may be busy with a capture', 0);
      }
      // Network or other errors
      throw new ApiError(`Network error: ${error instanceof Error ? error.message : 'Unknown error'}`, 0);
    } finally {
      clearTimeout(timeoutId);
    }
  }

  // Get session status
  async getSessionStatus(sessionId: string): Promise<SessionStatus> {
    return this.request<SessionStatus>(`/probes/${sessionId}/status`);
  }

  // List all sessions
  async listSessions(): Promise<SessionListItem[]> {
    return this.request<SessionListItem[]>('/probes');
  }

  // Get session details
  async getSessionDetails(sessionId: string): Promise<SessionDetailResponse> {
    return this.request<SessionDetailResponse>(`/probes/${sessionId}`);
  }

  /**
   * Utility method to poll session status until completion
   * @param sessionId - The session to poll
   * @param onProgress - Callback for progress updates
   * @param pollInterval - Polling interval in milliseconds
   * @param maxAttempts - Maximum polling attempts to prevent infinite loops
   */
  async pollSessionUntilComplete(
    sessionId: string,
    onProgress?: (status: SessionStatus) => void,
    pollInterval: number = 2000,
    maxAttempts: number = 300  // 10 minutes at 2s intervals
  ): Promise<SessionStatus> {
    return new Promise((resolve, reject) => {
      let attempts = 0;

      const poll = async () => {
        try {
          attempts++;
          
          if (attempts > maxAttempts) {
            reject(new Error(`Polling timeout after ${maxAttempts} attempts`));
            return;
          }

          const status = await this.getSessionStatus(sessionId);
          onProgress?.(status);

          if (status.state === 'completed') {
            resolve(status);
          } else if (status.state === 'failed') {
            reject(new Error('Session execution failed'));
          } else {
            // Continue polling for 'pending' or 'running' states
            setTimeout(poll, pollInterval);
          }
        } catch (error) {
          reject(error);
        }
      };

      poll();
    });
  }

  /**
   * Load pre-computed 3D trajectory points for a clustering schema.
   * Returns 404 if the schema was built before trajectory_points.json existed —
   * caller should display a message asking the user to rebuild via /cluster.
   */
  async getTrajectoryEmbedding(
    sessionId: string,
    schemaName: string
  ): Promise<TrajectoryPointsResponse> {
    return this.request<TrajectoryPointsResponse>(
      `/probes/sessions/${sessionId}/clusterings/${schemaName}/trajectory`
    );
  }

  /**
   * Archive a clustering schema (move to _archive/<name>_<ts>/).
   * Reversible by moving the directory back manually.
   */
  async archiveClustering(
    sessionId: string,
    schemaName: string
  ): Promise<{ archived: string; archive_path: string }> {
    return this.request(
      `/probes/sessions/${sessionId}/clusterings/${schemaName}/archive`,
      { method: 'POST' }
    );
  }

  /**
   * Delete a clustering schema. Pass force=true to override the safety check
   * when reports or element_descriptions reference the schema.
   */
  async deleteClustering(
    sessionId: string,
    schemaName: string,
    force = false
  ): Promise<{ deleted: string }> {
    const qs = force ? '?force=true' : '';
    return this.request(
      `/probes/sessions/${sessionId}/clusterings/${schemaName}${qs}`,
      { method: 'DELETE' }
    );
  }

  /**
   * Run a sentence experiment from a predefined sentence set
   * @param request - Sentence experiment request with sentence_set_name
   * @returns Session info with labels and counts
   */
  async runSentenceExperiment(request: SentenceExperimentRequest): Promise<SentenceExperimentResponse> {
    return this.request<SentenceExperimentResponse>('/probes/sentence-experiment', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }
  // --- Lenses (lenses and legacy schemas through one shape; `legacy` picks which) ---

  async listLenses(sessionId: string): Promise<LensSummary[]> {
    return this.request<LensSummary[]>(`/sessions/${sessionId}/lenses`);
  }

  // `outputAxes` groups the output column by those output axes instead of the output category.
  async getLensFlows(sessionId: string, name: string, legacy: boolean, outputAxes: string[] = []): Promise<LensFlows> {
    const params = new URLSearchParams({ legacy: String(legacy) });
    if (outputAxes.length) params.set('output_axes', outputAxes.join(','));
    return this.request<LensFlows>(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/flows?${params}`);
  }

  async getLensExpertFlows(sessionId: string, name: string, legacy: boolean, rank: number,
                           outputAxes: string[] = []): Promise<LensFlows> {
    const params = new URLSearchParams({ legacy: String(legacy), rank: String(rank) });
    if (outputAxes.length) params.set('output_axes', outputAxes.join(','));
    return this.request<LensFlows>(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/expert-flows?${params}`);
  }

  async getLensMembers(sessionId: string, name: string, legacy: boolean, query: MembersQuery): Promise<LensMembersPage> {
    const params = new URLSearchParams({ legacy: String(legacy) });
    for (const [key, value] of Object.entries(query)) {
      if (value !== undefined) params.set(key, String(value));
    }
    return this.request<LensMembersPage>(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/members?${params}`);
  }

  async getLensFingerprint(sessionId: string, name: string, legacy: boolean, who: Population): Promise<Fingerprint> {
    const params = new URLSearchParams({ legacy: String(legacy) });
    for (const [key, value] of Object.entries(who)) if (value !== undefined) params.set(key, String(value));
    return this.request<Fingerprint>(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/fingerprint?${params}`);
  }

  async getLensTrajectory(sessionId: string, name: string, legacy: boolean): Promise<TrajectoryPointsResponse> {
    return this.request<TrajectoryPointsResponse>(
      `/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/trajectory?legacy=${legacy}`);
  }

  async getLens(sessionId: string, name: string, legacy: boolean): Promise<LensDetail> {
    return this.request<LensDetail>(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}?legacy=${legacy}`);
  }

  // --- Building lenses ---

  async getLensOptions(sessionId: string): Promise<LensOptions> {
    return this.request<LensOptions>(`/captures/${sessionId}/lens-options`);
  }

  async getLensMethods(): Promise<LensMethods> {
    return this.request<LensMethods>('/lenses/methods');
  }

  // Starts a build in the background; the job's id comes back at once
  async buildLens(body: LensBuildBody): Promise<{ job_id: string; session_id: string; name: string }> {
    return this.request('/lenses', { method: 'POST', body: JSON.stringify(body) });
  }

  // A new draft version: the lens's trees cut at another k (one for all, per layer, or a method)
  async newLensVersion(sessionId: string, name: string,
                       body: { k?: number; k_per_layer?: number[]; k_auto?: string }): Promise<LensVersion> {
    return this.request<LensVersion>(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/versions`,
      { method: 'POST', body: JSON.stringify(body) });
  }

  // Scores the lens on held-out data, with its k profile, in the background
  async validateLens(sessionId: string, name: string,
                     body: { family_field?: string; n_folds?: number; seeds?: number } = {}): Promise<{ job_id: string }> {
    return this.request(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/validate`,
      { method: 'POST', body: JSON.stringify(body) });
  }

  // Tunes a UMAP lens in the background: a search over its settings and k per layer, then the
  // tuned lens is built and validated (DESIGN.md C4)
  async tuneLens(sessionId: string, name: string, body: TuneBody): Promise<{ job_id: string; session_id: string; source: string; name: string }> {
    return this.request(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/tune`,
      { method: 'POST', body: JSON.stringify(body) });
  }

  async getLensSearch(sessionId: string, name: string): Promise<LensSearch> {
    return this.request<LensSearch>(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/search`);
  }

  async getLensValidation(sessionId: string, name: string): Promise<Validation> {
    return this.request<Validation>(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/validation`);
  }

  // Where the lens and raw space disagree (needs the lens validated)
  async getLensMarks(sessionId: string, name: string): Promise<LensMarks> {
    return this.request<LensMarks>(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/marks`);
  }

  // Starts building a mass-mean lens: label A against label B
  async buildMassMean(body: { session_id: string; name: string; label_a: string; label_b: string;
                              token_position?: number; created_by: string }): Promise<{ job_id: string }> {
    return this.request('/lenses/mass-mean', { method: 'POST', body: JSON.stringify(body) });
  }

  async getMassMeanValidation(sessionId: string, name: string): Promise<MassMeanValidation> {
    return this.request<MassMeanValidation>(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/validation`);
  }

  // Works out what comes with each node (a mass-mean lens: each layer) in the background
  async computeLensDetails(sessionId: string, name: string): Promise<{ job_id: string }> {
    return this.request(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/details`,
      { method: 'POST', body: JSON.stringify({}) });
  }

  // The current version's node details, or a mass-mean lens's layer details (404 until worked out)
  async getLensDetails(sessionId: string, name: string): Promise<LensNodeDetails | MassMeanDetails> {
    return this.request<LensNodeDetails | MassMeanDetails>(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/details`);
  }

  // Freezes a version with its keywords
  async saveLensVersion(sessionId: string, name: string, version: string, keywords: string[]): Promise<LensVersion> {
    return this.request<LensVersion>(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/save`,
      { method: 'POST', body: JSON.stringify({ version, keywords }) });
  }

  // --- LLM analysis ---

  // Writes cards in the background: these card ids, or a save's plan when none are given
  async startAnalysis(sessionId: string, name: string, cards: string[], budget: number): Promise<{ job_id: string }> {
    return this.request(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/analysis`,
      { method: 'POST', body: JSON.stringify({ cards, budget }) });
  }

  // The current version's cards in brief
  async listCards(sessionId: string, name: string): Promise<{ version: string; cards: { card_id: string }[] }> {
    return this.request(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/cards`);
  }

  // A card on the current version, with the facts it cites (404 until written)
  async getCard(sessionId: string, name: string, cardId: string): Promise<Card> {
    return this.request<Card>(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/cards/${cardId}`);
  }

  async askQuestion(sessionId: string, name: string, cardId: string, question: string): Promise<{ job_id: string }> {
    return this.request(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/ask`,
      { method: 'POST', body: JSON.stringify({ card_id: cardId, question }) });
  }

  async listQuestions(sessionId: string, name: string, cardId: string): Promise<{ questions: QuestionAnswer[] }> {
    return this.request(`/sessions/${sessionId}/lenses/${encodeURIComponent(name)}/questions?card_id=${cardId}`);
  }

  async getAnalystTests(): Promise<AnalystTests> {
    return this.request<AnalystTests>('/analysts/tests');
  }

  async startAnalystTests(sessionId: string, name: string): Promise<{ job_id: string }> {
    return this.request('/analysts/tests', { method: 'POST', body: JSON.stringify({ session_id: sessionId, name }) });
  }

  // --- Background jobs ---

  async listJobs(active = false): Promise<JobView[]> {
    return this.request<JobView[]>(`/jobs${active ? '?active=true' : ''}`);
  }

  async getJob(jobId: string): Promise<JobView> {
    return this.request<JobView>(`/jobs/${jobId}`);
  }

  async cancelJob(jobId: string): Promise<JobView> {
    return this.request<JobView>(`/jobs/${jobId}/cancel`, { method: 'POST' });
  }

  /**
   * List available clustering schemas for a session
   */
  async listClusterings(sessionId: string): Promise<{ clusterings: ClusteringSchema[] }> {
    return this.request(`/probes/sessions/${sessionId}/clusterings`);
  }

  /**
   * Get clustering schema details including reports
   */
  async getClusteringDetails(sessionId: string, schemaName: string): Promise<{
    meta: ClusteringSchema;
    probe_assignments?: Record<string, Record<string, number>>;
    reports?: Record<string, string>;
    element_descriptions?: Record<string, string>;
  }> {
    return this.request(`/probes/sessions/${sessionId}/clusterings/${schemaName}`);
  }
}

// Export singleton instance
export const apiClient = new ConceptMriApiClient();
export default apiClient;