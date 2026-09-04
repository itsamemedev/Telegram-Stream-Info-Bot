/**
 * @name Information exposure through an exception (NIGHTCRAWLER)
 * @description Wie py/stack-trace-exposure, aber Rueckgaben von
 *              nc.fehlertext.nach_aussen gelten als gesaeubert.
 *              Siehe NcSanitizer.qll fuer die Begruendung und die Messung.
 * @kind path-problem
 * @problem.severity error
 * @security-severity 5.4
 * @precision high
 * @id nc/stack-trace-exposure
 * @tags security
 *       external/cwe/cwe-209
 *       external/cwe/cwe-497
 */

import python
import NcSanitizer
import semmle.python.security.dataflow.StackTraceExposureQuery
import StackTraceExposureFlow::PathGraph

from StackTraceExposureFlow::PathNode source, StackTraceExposureFlow::PathNode sink
where StackTraceExposureFlow::flowPath(source, sink)
select sink.getNode(), source, sink,
  "$@ flows to this location and may be exposed to an external user.", source.getNode(),
  "Stack trace information"
