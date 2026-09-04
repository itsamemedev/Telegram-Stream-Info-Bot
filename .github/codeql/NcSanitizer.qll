/**
 * v4.2-W3: nc.fehlertext.nach_aussen als Saeuberer fuer
 * py/stack-trace-exposure.
 *
 * Die Funktion nimmt den Wortlaut einer Ausnahme, schreibt ihn ins Log und
 * gibt nach aussen nur die gekuerzte, geschwaerzte Fassung zurueck:
 *
 *   roh    : [Errno 2] No such file: '/home/ubuntu/tiktok-bot/rec/x.mp4'
 *   aussen : FileNotFoundError: [Errno 2] No such file: '<x.mp4>'
 *   roh    : HTTP 401 von kick.com: token=abc123def456ghi789
 *   aussen : RuntimeError: HTTP 401 von kick.com: token=<geschwaerzt>
 *
 * Die Blueprints rufen sie ueber den lokalen Namen `_fehler_text`; beide
 * Namen zaehlen. Der Vertrag _test_w30_fehlertext_und_offenes_deck haelt
 * fest, dass es genau diese zwei sind — laeuft die Liste hier und dort
 * auseinander, faellt still eine Barriere weg und niemand sieht es.
 */

import python
import semmle.python.dataflow.new.DataFlow
import semmle.python.security.dataflow.StackTraceExposureCustomizations

class NcFehlertextSanitizer extends StackTraceExposure::Sanitizer {
  NcFehlertextSanitizer() {
    exists(DataFlow::CallCfgNode c |
      c.getFunction().asCfgNode().(NameNode).getId() in ["nach_aussen", "_fehler_text"] or
      c.getFunction().(DataFlow::AttrRead).getAttributeName() = "nach_aussen"
    |
      this = c
    )
  }
}
