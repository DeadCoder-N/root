import { X, Database, AlertTriangle, Download, Shield, Lock, Activity } from 'lucide-react';
import { useState } from 'react';

interface APISecurityModalProps {
  isOpen: boolean;
  onClose: () => void;
}

interface ScanResult {
  target_url: string;
  api_type: string;
  scan_date: string;
  scan_duration: string;
  vulnerability_count: number;
  severity_counts: {
    CRITICAL: number;
    HIGH: number;
    MEDIUM: number;
    LOW: number;
  };
  risk_score: number;
  risk_level: string;
  vulnerabilities: Array<{
    type: string;
    severity: string;
    description: string;
    evidence: string;
    fix_prompt?: string;
  }>;
}

export default function APISecurityModal({ isOpen, onClose }: APISecurityModalProps) {
  const [targetUrl, setTargetUrl] = useState('');
  const [apiType, setApiType] = useState('REST');
  const [authToken, setAuthToken] = useState('');
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState<ScanResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [reportId, setReportId] = useState<string | null>(null);

  if (!isOpen) {
    if (scanResult || error) {
      setTimeout(() => {
        setScanResult(null);
        setError(null);
        setTargetUrl('');
        setAuthToken('');
      }, 300);
    }
    return null;
  }

  const handleScan = async () => {
    if (!targetUrl.trim()) {
      setError('⚠️ Enter an API endpoint URL');
      return;
    }

    setIsScanning(true);
    setError(null);
    setScanResult(null);

    try {
      const response = await fetch('http://localhost:5004/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          target_url: targetUrl,
          api_type: apiType,
          auth_token: authToken || undefined
        })
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setScanResult(data.results);
        setReportId(data.report_id);
      } else {
        throw new Error(data.message || 'Scan failed');
      }
    } catch (err: any) {
      setError(`❌ Connection failed. Start backend: cd security-toolkit/tool-04-api-security-tester/backend && python3 app.py`);
    } finally {
      setIsScanning(false);
    }
  };

  const downloadReport = async () => {
    if (!reportId) return;
    try {
      const response = await fetch(`http://localhost:5004/api/download/${reportId}`);
      if (!response.ok) throw new Error('Download failed');
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `api_security_${reportId}.pdf`;
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
    return colors[severity as keyof typeof colors] || 'text-gray-500 bg-gray-500/10 border-gray-500/30';
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div className="bg-secondary border border-accent-teal/30 rounded-2xl w-full max-w-6xl max-h-[90vh] overflow-hidden shadow-2xl">
        <div className="bg-gradient-to-r from-blue-500/20 to-indigo-500/20 border-b border-accent-teal/30 p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-lg flex items-center justify-center">
                <Database className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold gradient-text">API Security Tester</h2>
                <p className="text-sm text-text-muted font-mono">OWASP API Top 10 Scanner</p>
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
                <Database className="w-4 h-4 inline mr-2" />API Endpoint URL
              </label>
              <input
                type="text"
                value={targetUrl}
                onChange={(e) => setTargetUrl(e.target.value)}
                placeholder="https://api.example.com/v1/users"
                className="w-full px-4 py-3 bg-tertiary border border-accent-teal/30 rounded-lg focus:outline-none focus:border-accent-teal text-text-primary placeholder-text-muted font-mono text-sm"
                disabled={isScanning}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold text-accent-teal mb-2">API Type</label>
                <select
                  value={apiType}
                  onChange={(e) => setApiType(e.target.value)}
                  className="w-full px-4 py-3 bg-tertiary border border-accent-teal/30 rounded-lg focus:outline-none focus:border-accent-teal text-text-primary"
                  disabled={isScanning}
                >
                  <option value="REST">REST API</option>
                  <option value="GraphQL">GraphQL</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-semibold text-accent-teal mb-2">
                  <Lock className="w-4 h-4 inline mr-2" />Auth Token (Optional)
                </label>
                <input
                  type="text"
                  value={authToken}
                  onChange={(e) => setAuthToken(e.target.value)}
                  placeholder="Bearer token..."
                  className="w-full px-4 py-3 bg-tertiary border border-accent-teal/30 rounded-lg focus:outline-none focus:border-accent-teal text-text-primary placeholder-text-muted font-mono text-sm"
                  disabled={isScanning}
                />
              </div>
            </div>

            <button
              onClick={handleScan}
              disabled={isScanning || !targetUrl.trim()}
              className="w-full py-3 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-lg font-semibold hover:shadow-lg hover:shadow-blue-500/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isScanning ? (
                <><div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin inline-block mr-2"></div>Testing API...</>
              ) : (
                <><Shield className="w-5 h-5 inline mr-2" />Start Security Test</>
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

          {scanResult && (
            <div className="space-y-6">
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <div className="glass-card p-4 text-center">
                  <p className="text-3xl font-bold text-accent-teal">{scanResult.vulnerability_count}</p>
                  <p className="text-xs text-text-muted mt-1">Total</p>
                </div>
                <div className="glass-card p-4 text-center">
                  <p className="text-3xl font-bold text-red-500">{scanResult.severity_counts.CRITICAL}</p>
                  <p className="text-xs text-text-muted mt-1">Critical</p>
                </div>
                <div className="glass-card p-4 text-center">
                  <p className="text-3xl font-bold text-orange-500">{scanResult.severity_counts.HIGH}</p>
                  <p className="text-xs text-text-muted mt-1">High</p>
                </div>
                <div className="glass-card p-4 text-center">
                  <p className="text-3xl font-bold text-yellow-500">{scanResult.severity_counts.MEDIUM}</p>
                  <p className="text-xs text-text-muted mt-1">Medium</p>
                </div>
                <div className="glass-card p-4 text-center">
                  <p className="text-3xl font-bold text-green-500">{scanResult.severity_counts.LOW}</p>
                  <p className="text-xs text-text-muted mt-1">Low</p>
                </div>
              </div>

              <div className={`glass-card p-6 border-l-4 ${getSeverityColor(scanResult.risk_level)}`}>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-text-muted mb-1">Risk Score</p>
                    <p className={`text-3xl font-bold ${getSeverityColor(scanResult.risk_level).split(' ')[0]}`}>
                      {scanResult.risk_score}/100
                    </p>
                  </div>
                  <button onClick={downloadReport} className="px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-lg font-medium hover:shadow-lg transition-all flex items-center space-x-2">
                    <Download className="w-4 h-4" /><span>Download PDF</span>
                  </button>
                </div>
              </div>

              <div className="glass-card p-6">
                <h3 className="text-lg font-bold text-accent-teal mb-4 flex items-center">
                  <Activity className="w-5 h-5 mr-2" />
                  OWASP API Security Vulnerabilities
                </h3>
                <div className="space-y-3">
                  {scanResult.vulnerabilities.map((vuln, index) => (
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

          {!scanResult && !isScanning && !error && (
            <div className="text-center py-16">
              <Database className="w-20 h-20 text-blue-500 mx-auto mb-6" />
              <h3 className="text-2xl font-bold text-accent-teal mb-4">Test Your API Security</h3>
              <p className="text-text-muted max-w-2xl mx-auto mb-6">
                Comprehensive testing for OWASP API Top 10 vulnerabilities including BOLA, authentication bypass, mass assignment, and more
              </p>
              <div className="grid grid-cols-2 gap-4 max-w-2xl mx-auto text-sm">
                <div className="glass-card p-4">
                  <p className="font-semibold text-accent-teal mb-2">✓ BOLA Testing</p>
                  <p className="text-xs text-text-muted">Broken Object Level Authorization</p>
                </div>
                <div className="glass-card p-4">
                  <p className="font-semibold text-accent-teal mb-2">✓ Auth Bypass</p>
                  <p className="text-xs text-text-muted">Authentication vulnerabilities</p>
                </div>
                <div className="glass-card p-4">
                  <p className="font-semibold text-accent-teal mb-2">✓ Rate Limiting</p>
                  <p className="text-xs text-text-muted">Missing rate limits</p>
                </div>
                <div className="glass-card p-4">
                  <p className="font-semibold text-accent-teal mb-2">✓ Mass Assignment</p>
                  <p className="text-xs text-text-muted">Excessive data exposure</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
