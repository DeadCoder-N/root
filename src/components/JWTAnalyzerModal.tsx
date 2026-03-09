import { X, Key, AlertTriangle, Download, Shield, Lock } from 'lucide-react';
import { useState } from 'react';

interface JWTAnalyzerModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function JWTAnalyzerModal({ isOpen, onClose }: JWTAnalyzerModalProps) {
  const [token, setToken] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [reportId, setReportId] = useState<string | null>(null);

  if (!isOpen) {
    if (result || error) {
      setTimeout(() => { setResult(null); setError(null); setToken(''); }, 300);
    }
    return null;
  }

  const handleAnalyze = async () => {
    if (!token.trim()) {
      setError('⚠️ Enter a JWT token');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:5005/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token })
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setResult(data.results);
        setReportId(data.report_id);
      }
    } catch (err: any) {
      setError(`❌ Connection failed. Start backend: cd security-toolkit/tool-05-jwt-analyzer/backend && python3 app.py`);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const downloadReport = async () => {
    if (!reportId) return;
    try {
      const response = await fetch(`http://localhost:5005/api/download/${reportId}`);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `jwt_analysis_${reportId}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('❌ Download failed');
    }
  };

  const getSeverityColor = (severity: string) => {
    const colors = {
      CRITICAL: 'text-red-500 bg-red-500/10 border-red-500/30',
      HIGH: 'text-orange-500 bg-orange-500/10 border-orange-500/30',
      MEDIUM: 'text-yellow-500 bg-yellow-500/10 border-yellow-500/30',
      LOW: 'text-green-500 bg-green-500/10 border-green-500/30'
    };
    return colors[severity as keyof typeof colors] || 'text-gray-500';
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div className="bg-secondary border border-accent-teal/30 rounded-2xl w-full max-w-6xl max-h-[90vh] overflow-hidden shadow-2xl">
        <div className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 border-b border-accent-teal/30 p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                <Key className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold gradient-text">JWT Analyzer</h2>
                <p className="text-sm text-text-muted font-mono">Token Security Scanner</p>
              </div>
            </div>
            <button onClick={onClose} className="w-10 h-10 rounded-lg bg-tertiary hover:bg-tertiary/80 transition-colors flex items-center justify-center">
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
          <div className="space-y-4 mb-6">
            <div>
              <label className="block text-sm font-semibold text-accent-teal mb-2">
                <Key className="w-4 h-4 inline mr-2" />JWT Token
              </label>
              <textarea
                value={token}
                onChange={(e) => setToken(e.target.value)}
                placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                className="w-full px-4 py-3 bg-tertiary border border-accent-teal/30 rounded-lg focus:outline-none focus:border-accent-teal text-text-primary placeholder-text-muted font-mono text-sm h-32"
                disabled={isAnalyzing}
              />
            </div>

            <button
              onClick={handleAnalyze}
              disabled={isAnalyzing || !token.trim()}
              className="w-full py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-semibold hover:shadow-lg hover:shadow-purple-500/50 transition-all disabled:opacity-50"
            >
              {isAnalyzing ? (
                <><div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin inline-block mr-2"></div>Analyzing...</>
              ) : (
                <><Shield className="w-5 h-5 inline mr-2" />Analyze Token</>
              )}
            </button>
          </div>

          {error && (
            <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 mb-6">
              <div className="flex items-start space-x-3">
                <AlertTriangle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-text-muted font-mono">{error}</p>
              </div>
            </div>
          )}

          {result && (
            <div className="space-y-6">
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <div className="glass-card p-4 text-center">
                  <p className="text-3xl font-bold text-accent-teal">{result.vulnerability_count}</p>
                  <p className="text-xs text-text-muted mt-1">Total</p>
                </div>
                <div className="glass-card p-4 text-center">
                  <p className="text-3xl font-bold text-red-500">{result.severity_counts?.CRITICAL || 0}</p>
                  <p className="text-xs text-text-muted mt-1">Critical</p>
                </div>
                <div className="glass-card p-4 text-center">
                  <p className="text-3xl font-bold text-orange-500">{result.severity_counts?.HIGH || 0}</p>
                  <p className="text-xs text-text-muted mt-1">High</p>
                </div>
                <div className="glass-card p-4 text-center">
                  <p className="text-3xl font-bold text-yellow-500">{result.severity_counts?.MEDIUM || 0}</p>
                  <p className="text-xs text-text-muted mt-1">Medium</p>
                </div>
                <div className="glass-card p-4 text-center">
                  <p className="text-3xl font-bold text-green-500">{result.severity_counts?.LOW || 0}</p>
                  <p className="text-xs text-text-muted mt-1">Low</p>
                </div>
              </div>

              <div className={`glass-card p-6 border-l-4 ${getSeverityColor(result.risk_level)}`}>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-text-muted mb-1">Risk Score</p>
                    <p className={`text-3xl font-bold ${getSeverityColor(result.risk_level).split(' ')[0]}`}>
                      {result.risk_score}/100
                    </p>
                  </div>
                  <button onClick={downloadReport} className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-medium hover:shadow-lg transition-all flex items-center space-x-2">
                    <Download className="w-4 h-4" /><span>Download PDF</span>
                  </button>
                </div>
              </div>

              <div className="glass-card p-6">
                <h3 className="text-lg font-bold text-accent-teal mb-4">JWT Vulnerabilities</h3>
                <div className="space-y-3">
                  {result.vulnerabilities?.map((vuln: any, index: number) => (
                    <div key={index} className={`p-4 rounded-lg border ${getSeverityColor(vuln.severity)}`}>
                      <div className="flex items-start justify-between mb-2">
                        <p className="font-semibold text-text-primary">{vuln.type}</p>
                        <span className={`px-3 py-1 rounded-full text-xs font-bold ${getSeverityColor(vuln.severity)}`}>
                          {vuln.severity}
                        </span>
                      </div>
                      <p className="text-sm text-text-muted mb-2">{vuln.description}</p>
                      {vuln.fix_prompt && (
                        <div className="mt-2 bg-accent-teal/10 border border-accent-teal/30 rounded p-2">
                          <p className="text-xs text-accent-teal font-semibold mb-1">💡 Fix:</p>
                          <p className="text-xs text-text-secondary">{vuln.fix_prompt}</p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {!result && !isAnalyzing && !error && (
            <div className="text-center py-16">
              <Key className="w-20 h-20 text-purple-500 mx-auto mb-6" />
              <h3 className="text-2xl font-bold text-accent-teal mb-4">Analyze JWT Security</h3>
              <p className="text-text-muted max-w-2xl mx-auto mb-6">
                Test JWT tokens for algorithm none attack, weak secrets, expiration issues, and signature validation
              </p>
              <div className="grid grid-cols-2 gap-4 max-w-2xl mx-auto text-sm">
                <div className="glass-card p-4">
                  <p className="font-semibold text-accent-teal mb-2">✓ Algorithm Testing</p>
                  <p className="text-xs text-text-muted">None attack, confusion</p>
                </div>
                <div className="glass-card p-4">
                  <p className="font-semibold text-accent-teal mb-2">✓ Secret Strength</p>
                  <p className="text-xs text-text-muted">Weak secret detection</p>
                </div>
                <div className="glass-card p-4">
                  <p className="font-semibold text-accent-teal mb-2">✓ Claims Validation</p>
                  <p className="text-xs text-text-muted">Expiration, sensitive data</p>
                </div>
                <div className="glass-card p-4">
                  <p className="font-semibold text-accent-teal mb-2">✓ Signature Check</p>
                  <p className="text-xs text-text-muted">Verification testing</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
