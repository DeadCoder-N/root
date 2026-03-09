import { X, Shield, AlertTriangle, Download, Github, Folder, Globe, Zap, Terminal } from 'lucide-react';
import { useState } from 'react';

interface CodeAnalyzerModalProps {
  isOpen: boolean;
  onClose: () => void;
}

interface ScanResult {
  scan_date: string;
  target: string;
  scan_type: string;
  total_vulnerabilities: number;
  severity_breakdown: {
    CRITICAL: number;
    HIGH: number;
    MEDIUM: number;
    LOW: number;
  };
  vulnerabilities: Array<{
    type: string;
    severity: string;
    file: string;
    line?: number;
    secret_type?: string;
    package?: string;
    version?: string;
    description?: string;
    cwe?: string;
    fix_prompt?: string;
  }>;
}

export default function CodeAnalyzerModal({ isOpen, onClose }: CodeAnalyzerModalProps) {
  const [targetUrl, setTargetUrl] = useState('');
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState<ScanResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [scanProgress, setScanProgress] = useState<{step: string; percent: number} | null>(null);

  if (!isOpen) {
    // Reset state when modal closes
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
      setError('⚠️ Enter a GitHub URL or website to analyze');
      return;
    }

    setIsScanning(true);
    setError(null);
    setScanResult(null);
    setScanProgress({ step: 'Initializing scan...', percent: 10 });

    try {
      setScanProgress({ step: 'Cloning repository...', percent: 20 });
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const response = await fetch('http://localhost:5001/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target: targetUrl, scan_type: 'github' })
      });

      setScanProgress({ step: '🔐 Scanning for secrets...', percent: 40 });
      await new Promise(resolve => setTimeout(resolve, 600));
      
      setScanProgress({ step: '📦 Checking dependencies...', percent: 60 });
      await new Promise(resolve => setTimeout(resolve, 600));
      
      setScanProgress({ step: '🔬 Analyzing code...', percent: 80 });
      await new Promise(resolve => setTimeout(resolve, 600));
      
      setScanProgress({ step: '📄 Generating report...', percent: 95 });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      
      setScanProgress({ step: '✅ Complete!', percent: 100 });
      await new Promise(resolve => setTimeout(resolve, 500));
      setScanResult(data);
    } catch (err: any) {
      setError(`❌ Connection failed. Start backend: cd security-toolkit/tool-1-vulnerability-scanner/backend && python3 app.py`);
    } finally {
      setIsScanning(false);
      setScanProgress(null);
    }
  };

  const downloadReport = async (format: 'json' | 'pdf') => {
    try {
      const response = await fetch(`http://localhost:5001/api/download?format=${format}`);
      if (!response.ok) throw new Error('Download failed');
      
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = `scan_report.${format}`;
      
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
    const { CRITICAL, HIGH } = scanResult.severity_breakdown;
    if (CRITICAL > 0) return 'CRITICAL';
    if (HIGH > 5) return 'HIGH';
    if (HIGH > 0) return 'MEDIUM';
    return 'LOW';
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div className="bg-secondary border border-accent-teal/30 rounded-2xl w-full max-w-6xl max-h-[90vh] overflow-hidden shadow-2xl">
        <div className="bg-gradient-to-r from-accent-teal/20 to-accent-purple/20 border-b border-accent-teal/30 p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-r from-accent-teal to-accent-purple rounded-lg flex items-center justify-center">
                <Terminal className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold gradient-text">Code Analyzer</h2>
                <p className="text-sm text-text-muted font-mono">Elite Security Scanner</p>
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
                <Zap className="w-4 h-4 inline mr-2" />Target URL
              </label>
              <input
                type="text"
                value={targetUrl}
                onChange={(e) => setTargetUrl(e.target.value)}
                placeholder="https://github.com/username/repo or https://github.com/username/repo.git"
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
                  <><div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin inline-block mr-2"></div>Scanning...</>
                ) : (
                  <><Shield className="w-5 h-5 inline mr-2" />Analyze</> 
                )}
              </button>
            </div>

            <p className="text-xs text-text-muted mt-2">
              <Github className="w-3 h-3 inline mr-1" />
              Supports GitHub repositories only. For website scanning, use Web Crawler tool.
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
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <div className="glass-card p-4 text-center">
                  <p className="text-3xl font-bold text-accent-teal">{scanResult.total_vulnerabilities}</p>
                  <p className="text-xs text-text-muted mt-1">Total</p>
                </div>
                <div className="glass-card p-4 text-center">
                  <p className="text-3xl font-bold text-red-500">{scanResult.severity_breakdown.CRITICAL}</p>
                  <p className="text-xs text-text-muted mt-1">Critical</p>
                </div>
                <div className="glass-card p-4 text-center">
                  <p className="text-3xl font-bold text-orange-500">{scanResult.severity_breakdown.HIGH}</p>
                  <p className="text-xs text-text-muted mt-1">High</p>
                </div>
                <div className="glass-card p-4 text-center">
                  <p className="text-3xl font-bold text-yellow-500">{scanResult.severity_breakdown.MEDIUM}</p>
                  <p className="text-xs text-text-muted mt-1">Medium</p>
                </div>
                <div className="glass-card p-4 text-center">
                  <p className="text-3xl font-bold text-green-500">{scanResult.severity_breakdown.LOW}</p>
                  <p className="text-xs text-text-muted mt-1">Low</p>
                </div>
              </div>

              <div className={`glass-card p-6 border-l-4 ${getSeverityColor(getRiskLevel())}`}>
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <p className="text-sm text-text-muted mb-1">Overall Risk Level</p>
                    <p className={`text-3xl font-bold ${getSeverityColor(getRiskLevel()).split(' ')[0]}`}>{getRiskLevel()}</p>
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

              <div className="glass-card p-6">
                <h3 className="text-lg font-bold text-accent-teal mb-4">Vulnerability Types Detected</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-red-500/20 rounded-lg flex items-center justify-center">
                        <span className="text-xl">🔴</span>
                      </div>
                      <div>
                        <p className="font-semibold text-text-primary">Exposed Secrets</p>
                        <p className="text-xs text-text-muted">AWS keys, API keys, passwords, tokens</p>
                      </div>
                    </div>
                    <span className="text-2xl font-bold text-red-500">
                      {scanResult.vulnerabilities.filter(v => v.type === 'Exposed Secret').length}
                    </span>
                  </div>

                  <div className="flex items-center justify-between p-3 bg-orange-500/10 border border-orange-500/30 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-orange-500/20 rounded-lg flex items-center justify-center">
                        <span className="text-xl">🟠</span>
                      </div>
                      <div>
                        <p className="font-semibold text-text-primary">Outdated Dependencies</p>
                        <p className="text-xs text-text-muted">Old packages with known vulnerabilities</p>
                      </div>
                    </div>
                    <span className="text-2xl font-bold text-orange-500">
                      {scanResult.vulnerabilities.filter(v => v.type === 'Outdated Dependency' || v.type === 'Vulnerable Dependency').length}
                    </span>
                  </div>

                  <div className="flex items-center justify-between p-3 bg-yellow-500/10 border border-yellow-500/30 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-yellow-500/20 rounded-lg flex items-center justify-center">
                        <span className="text-xl">🟡</span>
                      </div>
                      <div>
                        <p className="font-semibold text-text-primary">Missing Security Headers</p>
                        <p className="text-xs text-text-muted">CSP, HSTS, X-Frame-Options, etc.</p>
                      </div>
                    </div>
                    <span className="text-2xl font-bold text-yellow-500">
                      {scanResult.vulnerabilities.filter(v => v.type === 'Missing Security Header').length}
                    </span>
                  </div>

                  <div className="flex items-center justify-between p-3 bg-green-500/10 border border-green-500/30 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-green-500/20 rounded-lg flex items-center justify-center">
                        <span className="text-xl">🟢</span>
                      </div>
                      <div>
                        <p className="font-semibold text-text-primary">Configuration Issues</p>
                        <p className="text-xs text-text-muted">Missing SRI, exposed files, CORS issues</p>
                      </div>
                    </div>
                    <span className="text-2xl font-bold text-green-500">
                      {scanResult.vulnerabilities.filter(v => v.type === 'Missing SRI' || v.type === 'Sensitive File Exposed' || v.type === 'Missing CSRF Protection').length}
                    </span>
                  </div>

                  <div className="flex items-center justify-between p-3 bg-blue-500/10 border border-blue-500/30 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
                        <span className="text-xl">🔵</span>
                      </div>
                      <div>
                        <p className="font-semibold text-text-primary">Code Vulnerabilities</p>
                        <p className="text-xs text-text-muted">SQL injection, XSS, dangerous functions</p>
                      </div>
                    </div>
                    <span className="text-2xl font-bold text-blue-500">
                      {scanResult.vulnerabilities.filter(v => v.type === 'Code Vulnerability' || v.type === 'Dangerous Function' || v.type === 'Potential SQL Injection' || v.type === 'Potential XSS').length}
                    </span>
                  </div>

                  <div className="flex items-center justify-between p-4 bg-accent-teal/10 border-2 border-accent-teal/50 rounded-lg mt-4">
                    <div className="flex items-center space-x-3">
                      <Shield className="w-8 h-8 text-accent-teal" />
                      <p className="font-bold text-lg text-text-primary">Total Vulnerabilities</p>
                    </div>
                    <span className="text-3xl font-bold text-accent-teal">{scanResult.total_vulnerabilities}</span>
                  </div>
                </div>
              </div>



              {/* Detailed Vulnerabilities - HIDDEN (included in PDF) */}
              {/* <div className="space-y-3">
                <h3 className="text-lg font-bold text-accent-teal">Detailed Vulnerabilities</h3>
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {scanResult.vulnerabilities.slice(0, 20).map((vuln, index) => (
                    <div key={index} className="glass-card p-4 hover:border-accent-teal/50 transition-colors">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center space-x-3">
                          <span className={`px-3 py-1 rounded-full text-xs font-bold border ${getSeverityColor(vuln.severity)}`}>{vuln.severity}</span>
                          <p className="font-semibold text-text-primary">{vuln.type}</p>
                        </div>
                        {vuln.cwe && <span className="text-xs text-text-muted font-mono bg-tertiary px-2 py-1 rounded">{vuln.cwe}</span>}
                      </div>
                      <div className="space-y-1 text-sm">
                        <p className="text-text-muted">
                          <Folder className="w-3 h-3 inline mr-1" />
                          <span className="font-mono">{vuln.file.split('/').pop()}</span>
                          {vuln.line && <span className="text-accent-teal ml-2">Line {vuln.line}</span>}
                        </p>
                        {vuln.secret_type && <p className="text-text-secondary">Type: {vuln.secret_type}</p>}
                        {vuln.package && <p className="text-text-secondary">Package: {vuln.package} {vuln.version}</p>}
                        {vuln.description && <p className="text-text-secondary">{vuln.description}</p>}
                        {vuln.fix_prompt && (
                          <div className="mt-2 bg-accent-teal/10 border border-accent-teal/30 rounded p-2">
                            <p className="text-xs text-accent-teal font-semibold mb-1">💡 How to Fix:</p>
                            <p className="text-xs text-text-secondary">{vuln.fix_prompt}</p>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                  {scanResult.vulnerabilities.length > 20 && (
                    <p className="text-center text-sm text-text-muted py-4">... and {scanResult.vulnerabilities.length - 20} more issues. Download full report for details.</p>
                  )}
                </div>
              </div> */}
            </div>
          )}

          {!scanResult && !isScanning && !error && (
            <div className="text-center py-16">
              <div className="max-w-2xl mx-auto space-y-6">
                <Shield className="w-20 h-20 text-accent-teal mx-auto mb-6" />
                
                <div className="space-y-4">
                  <h3 className="text-2xl font-bold text-accent-teal">How to Use Code Analyzer</h3>
                  
                  <div className="glass-card p-6 text-left space-y-4">
                    <div className="flex items-start space-x-3">
                      <div className="w-8 h-8 bg-accent-teal/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                        <span className="text-accent-teal font-bold">1</span>
                      </div>
                      <div>
                        <p className="font-semibold text-text-primary mb-1">Enter GitHub Repository URL</p>
                        <p className="text-sm text-text-muted">Example: https://github.com/username/repository</p>
                      </div>
                    </div>

                    <div className="flex items-start space-x-3">
                      <div className="w-8 h-8 bg-accent-teal/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                        <span className="text-accent-teal font-bold">2</span>
                      </div>
                      <div>
                        <p className="font-semibold text-text-primary mb-1">Click Analyze Button</p>
                        <p className="text-sm text-text-muted">The scanner will clone and analyze the repository</p>
                      </div>
                    </div>

                    <div className="flex items-start space-x-3">
                      <div className="w-8 h-8 bg-accent-teal/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                        <span className="text-accent-teal font-bold">3</span>
                      </div>
                      <div>
                        <p className="font-semibold text-text-primary mb-1">Review Results & Download Report</p>
                        <p className="text-sm text-text-muted">Get detailed vulnerability report in JSON or PDF format</p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-accent-teal/10 border border-accent-teal/30 rounded-lg p-4">
                    <p className="text-sm text-accent-teal font-semibold mb-2">🔍 What We Scan:</p>
                    <div className="grid grid-cols-2 gap-2 text-xs text-text-muted">
                      <div>• Exposed Secrets (API keys, tokens)</div>
                      <div>• Outdated Dependencies</div>
                      <div>• Security Headers</div>
                      <div>• Code Vulnerabilities</div>
                      <div>• Configuration Issues</div>
                      <div>• SQL Injection Risks</div>
                    </div>
                  </div>

                  <button
                    onClick={() => document.querySelector('input')?.focus()}
                    className="px-8 py-3 bg-gradient-to-r from-accent-teal to-accent-purple text-white rounded-lg font-semibold hover:shadow-lg hover:shadow-accent-teal/50 transition-all inline-flex items-center space-x-2"
                  >
                    <Shield className="w-5 h-5" />
                    <span>Start Analyzing</span>
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
