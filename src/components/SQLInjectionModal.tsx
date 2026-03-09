import { X, Shield, AlertTriangle, Download, Syringe, Zap, Terminal } from 'lucide-react';
import { useState } from 'react';

interface SQLInjectionModalProps {
  isOpen: boolean;
  onClose: () => void;
}

interface ScanResult {
  scan_date: string;
  target: string;
  total_vulnerabilities: number;
  parameters_tested: number;
  vulnerabilities: Array<{
    parameter: string;
    payload: string;
    type: string;
    severity: string;
    evidence: string;
    url: string;
  }>;
}

export default function SQLInjectionModal({ isOpen, onClose }: SQLInjectionModalProps) {
  const [targetUrl, setTargetUrl] = useState('');
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState<ScanResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [scanProgress, setScanProgress] = useState<{step: string; percent: number} | null>(null);

  if (!isOpen) {
    if (scanResult || error) {
      setTimeout(() => {
        setScanResult(null);
        setError(null);
        setTargetUrl('');
      }, 300);
    }
    return null;
  }

  const handleScan = async () => {
    if (!targetUrl.trim()) {
      setError('⚠️ Enter a URL with parameters to test');
      return;
    }

    if (!targetUrl.includes('?')) {
      setError('⚠️ URL must contain parameters (e.g., ?id=1 or ?q=test)');
      return;
    }

    setIsScanning(true);
    setError(null);
    setScanResult(null);
    setScanProgress({ step: 'Initializing scan...', percent: 10 });

    try {
      setScanProgress({ step: 'Testing error-based injection...', percent: 30 });
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const response = await fetch('http://localhost:5002/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target: targetUrl })
      });

      setScanProgress({ step: 'Testing union-based injection...', percent: 60 });
      await new Promise(resolve => setTimeout(resolve, 600));
      
      setScanProgress({ step: 'Testing time-based injection...', percent: 85 });
      await new Promise(resolve => setTimeout(resolve, 600));
      
      setScanProgress({ step: 'Generating report...', percent: 95 });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      
      setScanProgress({ step: '✅ Complete!', percent: 100 });
      await new Promise(resolve => setTimeout(resolve, 500));
      setScanResult(data);
    } catch (err: any) {
      setError(`❌ Connection failed. Start backend: cd security-toolkit/tool-2-sql-injection-tester/backend && python3 app.py`);
    } finally {
      setIsScanning(false);
      setScanProgress(null);
    }
  };

  const downloadReport = async (format: 'json' | 'pdf') => {
    try {
      const response = await fetch(`http://localhost:5002/api/download?format=${format}`);
      if (!response.ok) throw new Error('Download failed');
      
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = `sqli_report.${format}`;
      
      if (contentDisposition) {
        const match = contentDisposition.match(/filename="?([^"]+)"?/i);
        if (match && match[1]) {
          filename = match[1];
        }
      }
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
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

  const getRiskLevel = () => {
    if (!scanResult) return 'UNKNOWN';
    if (scanResult.total_vulnerabilities === 0) return 'SECURE';
    const hasCritical = scanResult.vulnerabilities.some(v => v.severity === 'CRITICAL');
    if (hasCritical) return 'CRITICAL';
    const hasHigh = scanResult.vulnerabilities.some(v => v.severity === 'HIGH');
    if (hasHigh) return 'HIGH';
    return 'MEDIUM';
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div className="bg-secondary border border-accent-teal/30 rounded-2xl w-full max-w-6xl max-h-[90vh] overflow-hidden shadow-2xl">
        <div className="bg-gradient-to-r from-accent-teal/20 to-accent-purple/20 border-b border-accent-teal/30 p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-r from-accent-teal to-accent-purple rounded-lg flex items-center justify-center">
                <Syringe className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold gradient-text">SQL Injection Tester</h2>
                <p className="text-sm text-text-muted font-mono">Database Security Scanner</p>
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
                <Zap className="w-4 h-4 inline mr-2" />Target URL (with parameters)
              </label>
              <input
                type="text"
                value={targetUrl}
                onChange={(e) => setTargetUrl(e.target.value)}
                placeholder="https://example.com/search?q=test or http://localhost:3002/search?q=test"
                className="w-full px-4 py-3 bg-tertiary border border-accent-teal/30 rounded-lg focus:outline-none focus:border-accent-teal text-text-primary placeholder-text-muted font-mono text-sm"
                disabled={isScanning}
              />
            </div>

            <div className="flex items-center justify-end">
              <button
                onClick={handleScan}
                disabled={isScanning || !targetUrl.trim()}
                className="px-8 py-3 bg-gradient-to-r from-accent-teal to-accent-purple text-white rounded-lg font-semibold hover:shadow-lg hover:shadow-accent-teal/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed mt-7"
              >
                {isScanning ? (
                  <><div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin inline-block mr-2"></div>Testing...</>
                ) : (
                  <><Shield className="w-5 h-5 inline mr-2" />Test for SQL Injection</> 
                )}
              </button>
            </div>

            <p className="text-xs text-text-muted mt-2">
              <Terminal className="w-3 h-3 inline mr-1" />
              Tests for error-based, union-based, and time-based SQL injection vulnerabilities.
            </p>
          </div>

          {isScanning && scanProgress && (
            <div className="bg-accent-teal/10 border border-accent-teal/30 rounded-lg p-6 mb-6">
              <div className="flex items-center justify-between mb-3">
                <p className="text-accent-teal font-semibold">{scanProgress.step}</p>
                <p className="text-accent-teal font-mono text-sm">{scanProgress.percent}%</p>
              </div>
              <div className="w-full bg-tertiary rounded-full h-2 overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-accent-teal to-accent-purple transition-all duration-500"
                  style={{ width: `${scanProgress.percent}%` }}
                ></div>
              </div>
            </div>
          )}

          {error && (
            <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 mb-6">
              <div className="flex items-start space-x-3">
                <AlertTriangle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="text-red-500 font-semibold mb-1">Error</p>
                  <p className="text-sm text-text-muted font-mono">{error}</p>
                </div>
              </div>
            </div>
          )}

          {scanResult && (
            <div className="space-y-6">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="glass-card p-4 text-center">
                  <p className="text-3xl font-bold text-accent-teal">{scanResult.total_vulnerabilities}</p>
                  <p className="text-xs text-text-muted mt-1">Vulnerabilities</p>
                </div>
                <div className="glass-card p-4 text-center">
                  <p className="text-3xl font-bold text-blue-500">{scanResult.parameters_tested}</p>
                  <p className="text-xs text-text-muted mt-1">Parameters Tested</p>
                </div>
                <div className="glass-card p-4 text-center">
                  <p className={`text-3xl font-bold ${getRiskLevel() === 'SECURE' ? 'text-green-500' : getRiskLevel() === 'CRITICAL' ? 'text-red-500' : 'text-orange-500'}`}>
                    {getRiskLevel()}
                  </p>
                  <p className="text-xs text-text-muted mt-1">Risk Level</p>
                </div>
                <div className="glass-card p-4 text-center">
                  <p className="text-3xl font-bold text-purple-500">{scanResult.vulnerabilities.length}</p>
                  <p className="text-xs text-text-muted mt-1">Issues Found</p>
                </div>
              </div>

              {scanResult.total_vulnerabilities > 0 ? (
                <div className="glass-card p-6 border-l-4 border-red-500">
                  <div className="flex items-center justify-between mb-6">
                    <div>
                      <p className="text-sm text-text-muted mb-1">Security Status</p>
                      <p className="text-3xl font-bold text-red-500">⚠️ VULNERABLE</p>
                      <p className="text-sm text-text-muted mt-2">SQL injection vulnerabilities detected. Immediate action required!</p>
                    </div>
                    <div className="flex space-x-2">
                      <button onClick={() => downloadReport('json')} className="px-4 py-2 bg-tertiary hover:bg-tertiary/80 rounded-lg text-sm font-medium transition-colors flex items-center space-x-2">
                        <Download className="w-4 h-4" /><span>JSON</span>
                      </button>
                      <button onClick={() => downloadReport('pdf')} className="px-4 py-2 bg-gradient-to-r from-accent-teal to-accent-purple text-white rounded-lg text-sm font-medium hover:shadow-lg transition-all flex items-center space-x-2">
                        <Download className="w-4 h-4" /><span>PDF Report</span>
                      </button>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="glass-card p-6 border-l-4 border-green-500">
                  <div className="flex items-center justify-between mb-6">
                    <div>
                      <p className="text-sm text-text-muted mb-1">Security Status</p>
                      <p className="text-3xl font-bold text-green-500">✅ SECURE</p>
                      <p className="text-sm text-text-muted mt-2">No SQL injection vulnerabilities detected.</p>
                    </div>
                    <div className="flex space-x-2">
                      <button onClick={() => downloadReport('json')} className="px-4 py-2 bg-tertiary hover:bg-tertiary/80 rounded-lg text-sm font-medium transition-colors flex items-center space-x-2">
                        <Download className="w-4 h-4" /><span>JSON</span>
                      </button>
                      <button onClick={() => downloadReport('pdf')} className="px-4 py-2 bg-gradient-to-r from-accent-teal to-accent-purple text-white rounded-lg text-sm font-medium hover:shadow-lg transition-all flex items-center space-x-2">
                        <Download className="w-4 h-4" /><span>PDF Report</span>
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {scanResult.vulnerabilities.length > 0 && (
                <div className="glass-card p-6">
                  <h3 className="text-lg font-bold text-accent-teal mb-4">Vulnerability Details</h3>
                  <div className="space-y-3">
                    {scanResult.vulnerabilities.map((vuln, index) => (
                      <div key={index} className="p-4 bg-tertiary rounded-lg border border-accent-teal/20 hover:border-accent-teal/50 transition-colors">
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center space-x-3">
                            <span className={`px-3 py-1 rounded-full text-xs font-bold border ${getSeverityColor(vuln.severity)}`}>
                              {vuln.severity}
                            </span>
                            <p className="font-semibold text-text-primary">{vuln.type}</p>
                          </div>
                        </div>
                        <div className="space-y-1 text-sm mt-3">
                          <p className="text-text-muted">
                            <span className="font-semibold text-accent-teal">Parameter:</span> <span className="font-mono">{vuln.parameter}</span>
                          </p>
                          <p className="text-text-muted">
                            <span className="font-semibold text-accent-teal">Payload:</span> <span className="font-mono text-xs bg-tertiary px-2 py-1 rounded">{vuln.payload}</span>
                          </p>
                          <p className="text-text-muted">
                            <span className="font-semibold text-accent-teal">Evidence:</span> {vuln.evidence}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="mt-4 p-4 bg-accent-teal/10 border border-accent-teal/30 rounded-lg">
                    <p className="text-sm text-accent-teal font-semibold mb-2">💡 Quick Fix:</p>
                    <p className="text-xs text-text-secondary">
                      Use prepared statements (parameterized queries) instead of string concatenation. 
                      Download the PDF report for detailed fix instructions and AI prompts.
                    </p>
                  </div>
                </div>
              )}
            </div>
          )}

          {!scanResult && !isScanning && !error && (
            <div className="text-center py-16">
              <div className="max-w-2xl mx-auto space-y-6">
                <Syringe className="w-20 h-20 text-accent-teal mx-auto mb-6" />
                
                <div className="space-y-4">
                  <h3 className="text-2xl font-bold text-accent-teal">How to Use SQL Injection Tester</h3>
                  
                  <div className="glass-card p-6 text-left space-y-4">
                    <div className="flex items-start space-x-3">
                      <div className="w-8 h-8 bg-accent-teal/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                        <span className="text-accent-teal font-bold">1</span>
                      </div>
                      <div>
                        <p className="font-semibold text-text-primary mb-1">Enter Target URL with Parameters</p>
                        <p className="text-sm text-text-muted">Example: https://example.com/search?q=test</p>
                      </div>
                    </div>

                    <div className="flex items-start space-x-3">
                      <div className="w-8 h-8 bg-accent-teal/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                        <span className="text-accent-teal font-bold">2</span>
                      </div>
                      <div>
                        <p className="font-semibold text-text-primary mb-1">Click Test Button</p>
                        <p className="text-sm text-text-muted">Tool will inject 60+ SQL payloads automatically</p>
                      </div>
                    </div>

                    <div className="flex items-start space-x-3">
                      <div className="w-8 h-8 bg-accent-teal/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                        <span className="text-accent-teal font-bold">3</span>
                      </div>
                      <div>
                        <p className="font-semibold text-text-primary mb-1">Review Results & Download Report</p>
                        <p className="text-sm text-text-muted">Get detailed report with AI fix prompts in simple English</p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-accent-teal/10 border border-accent-teal/30 rounded-lg p-4">
                    <p className="text-sm text-accent-teal font-semibold mb-2">🔍 What We Test:</p>
                    <div className="grid grid-cols-2 gap-2 text-xs text-text-muted">
                      <div>• Error-based SQL injection</div>
                      <div>• Union-based SQL injection</div>
                      <div>• Time-based blind injection</div>
                      <div>• Database fingerprinting</div>
                    </div>
                  </div>

                  <button
                    onClick={() => document.querySelector('input')?.focus()}
                    className="px-8 py-3 bg-gradient-to-r from-accent-teal to-accent-purple text-white rounded-lg font-semibold hover:shadow-lg hover:shadow-accent-teal/50 transition-all inline-flex items-center space-x-2"
                  >
                    <Shield className="w-5 h-5" />
                    <span>Start Testing</span>
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
