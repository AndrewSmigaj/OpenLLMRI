// jStat ships no type declarations; this covers the part the app uses.
declare module 'jStat' {
  const jStat: {
    chisquare: { cdf(x: number, dof: number): number }
  }
  export default jStat
}
