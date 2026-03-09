import { X, Zap, AlertTriangle, Download, Loader2 } from 'lucide-react';
import { useState } from 'react';

interface BusinessLogicModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function BusinessLogicModal({ isOpen, onClose }: BusinessLogicModalProps) {
  const [url, setUrl] = useState('');
  const [testType, setTestType] = useState('all');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [error, setError] = useState('');

  const handleTest = async () => {
    if (!url.trim()) {
      setError('Please enter an endpoint URL');
      return;
    }

    setLoading(true);
    setError('');
    setResults(null);

    try {
      const response = await fetch('http://localhost:5016/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url.trim(), test_type: testType }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Test failed');
      }

      setResults(data);
    } catch (err: any) {
      setError(err.message || 'Failed to test business logic');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!results) return;

    try {
      const response = await fetch('http://localhost:5016/api/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(results),
      });

      if (!response.ok) throw new Error('PDF generation failed');

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `business-logic-test-report-${Date.now()}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError('Failed to download PDF report');
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical': return 'text-red-500 bg-red-500/10 border-red-500/30';
      case 'high': return 'text-orange-500 bg-orange-500/10 border-orange-500/30';
      case 'medium': return 'text-yellow-500 bg-yellow-500/10 border-yellow-500/30';
      case 'low': return 'text-blue-500 bg-blue-500/10 border-blue-500/30';
      default: return 'text-gray-500 bg-gray-500/10 border-gray-500/30';
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-primary border border-white/10 rounded-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        <div className="bg-gradient-to-r from-yellow-500 to-orange-500 p-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Zap className="w-8 h-8 text-white" />
            <div>
              <h2 className="text-2xl font-bold text-white">Business Logic Tester</h2>
              <p className="text-white/80 text-sm">Test business logic vulnerabilities</p>
            </div>
          </div>
          <button onClick={onClose} className="text-white/80 hover:text-white transition-colors">
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Endpoint URL *</label>
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://example.com/api/checkout"
                className="w-full px-4 py-2 bg-secondary border border-white/10 rounded-lg focus:outline-none focus:border-yellow-500/50"
                disabled={loading}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Test Type</label>
              <select
                value={testType}
                onChange={(e) => setTestType(e.target.value)}
                className="w-full px-4 py-2 bg-secondary border border-white/10 rounded-lg focus:outline-none focus:border-yellow-500/50"
                disabled={loading}
              >
                <option value="all">All Tests</option>
                <option value="race_condition">Race Condition</option>
                <option value="price_manipulation">Price Manipulation</option>
                <option value="negative_values">Negative Values</option>
                <option value="parameter_tampering">Parameter Tampering</option>
              </select>
            </div>

            <button
              onClick={handleTest}
              disabled={loading}
              className="w-full bg-gradient-to-r from-yellow-500 to-orange-500 text-white py-3 rounded-lg font-medium hover:opacity-90 transition-opacity disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Testing Business Logic...
                </>
              ) : (
                <>
                  <Zap className="w-5 h-5" />
                  Test Business Logic
                </>
              )}
            </button>
          </div>

          {error && (
            <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
              <p className="text-red-500 text-sm">{error}</p>
            </div>
          )}

          {results && (
            <div className="space-y-6">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
                  <div className="text-2xl font-bold text-red-500">{results.summary?.critical || 0}</div>
                  <div className="text-sm text-text-muted">Critical</div>
                </div>
                <div className="p-4 bg-orange-500/10 border border-orange-500/30 rounded-lg">
                  <div className="text-2xl font-bold text-orange-500">{results.summary?.high || 0}</div>
                  <div className="text-sm text-text-muted">High</div>
                </div>
                <div className="p-4 bg-yellow-500/10 border border-yellow-500/30 rounded-lg">
                  <div className="text-2xl font-bold text-yellow-500">{results.summary?.medium || 0}</div>
                  <div className="text-sm text-text-muted">Medium</div>
                </div>
                <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg">
                  <div className="text-2xl font-bold text-blue-500">{results.summary?.low || 0}</div>
                  <div className="text-sm text-text-muted">Low</div>
                </div>
              </div>

              <div className="p-4 bg-secondary border border-white/10 rounded-lg">
                <div className="text-sm text-text-muted mb-1">Risk Score</div>
                <div className="text-3xl font-bold gradient-text">{results.risk_score}/100</div>
              </div>

              {results.vulnerabilities && results.vulnerabilities.length > 0 && (
                <div className="space-y-3">
                  <h3 className="text-lg font-semibold">Vulnerabilities Found</h3>
                  {results.vulnerabilities.map((vuln: any, index: number) => (
                    <div key={index} className="p-4 bg-secondary border border-white/10 rounded-lg space-y-2">
                      <div className="flex items-start justify-between gap-3">
                        <h4 className="font-medium flex-1">{vuln.title}</h4>
                        <span className={`text-xs px-2 py-1 rounded border ${getSeverityColor(vuln.severity)}`}>
                          {vuln.severity}
                        </span>
                      </div>
                      <p className="text-sm text-text-muted">{vuln.description}</p>
                      {vuln.fix_prompt && (
                        <div className="mt-2 p-3 bg-primary border border-yellow-500/30 rounded">
                          <div className="text-xs text-yellow-500 font-medium mb-1">Fix Recommendation:</div>
                          <p className="text-sm text-text-muted">{vuln.fix_prompt}</p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}

              <button
                onClick={handleDownloadPDF}
                className="w-full bg-secondary border border-white/10 text-white py-3 rounded-lg font-medium hover:bg-white/5 transition-colors flex items-center justify-center gap-2"
              >
                <Download className="w-5 h-5" />
                Download PDF Report
              </button>
            </div>
          )}

          {!results && !loading && !error && (
            <div className="text-center py-12 space-y-4">
              <Zap className="w-16 h-16 text-text-muted mx-auto opacity-50" />
              <div>
                <h3 className="text-lg font-semibold mb-2">How to Use</h3>
                <div className="text-sm text-text-muted space-y-2 max-w-md mx-auto text-left">
                  <p>• Enter the business logic endpoint URL</p>
                  <p>• Select specific test type or run all tests</p>
                  <p>• Tests race conditions, price manipulation, negative values</p>
                  <p>• Detects parameter tampering vulnerabilities</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
