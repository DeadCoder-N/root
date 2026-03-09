import { useState } from 'react';
import { X, Loader2, Shield, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';

interface ScannerModalProps {
  isOpen: boolean;
  onClose: () => void;
}

interface ScanResult {
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
    cwe: string;
  }>;
}

export default function ScannerModal({ isOpen, onClose }: ScannerModalProps) {
  const [repoUrl, setRepoUrl] = useState('');
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState<ScanResult | null>(null);
  const [error, setError] = useState('');

  const handleScan = async () => {
    if (!repoUrl.trim()) {
      setError('Please enter a GitHub repository URL');
      return;
    }

    // Validate GitHub URL
    const githubRegex = /^https:\/\/github\.com\/[\w-]+\/[\w.-]+(\.git)?$/;
    if (!githubRegex.test(repoUrl.trim())) {
      setError('Invalid GitHub URL. Format: https://github.com/username/repo');
      return;
    }

    setIsScanning(true);
    setError('');
    setScanResult(null);

    // Backend URLs (Railway primary, localhost fallback)
    const backends = [
      'https://root-production-2034.up.railway.app/api/scan', // Railway backend
      'http://localhost:5000/api/scan', // Fallback to local
    ];

    let lastError = '';

    for (const backendUrl of backends) {
      try {
        console.log(`Trying backend: ${backendUrl}`);
        
        const response = await fetch(backendUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ repo_url: repoUrl.trim() }),
          signal: AbortSignal.timeout(90000), // 90 second timeout
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Scan failed');
        }

        const data = await response.json();
        setScanResult(data);
        console.log(`✓ Scan successful using: ${backendUrl}`);
        return; // Success, exit loop
        
      } catch (err) {
        lastError = err instanceof Error ? err.message : 'Connection failed';
        console.log(`✗ Backend failed: ${backendUrl} - ${lastError}`);
        
        // If this was the last backend, show error
        if (backendUrl === backends[backends.length - 1]) {
          setError(
            `All backends failed. Last error: ${lastError}\n\n` +
            `💡 To use local backend:\n` +
            `1. Open terminal\n` +
            `2. cd ReportLab/backend\n` +
            `3. python app.py\n` +
            `4. Try scanning again`
          );
        }
        // Continue to next backend
      }
    }

    setIsScanning(false);
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'CRITICAL': return 'text-red-500';
      case 'HIGH': return 'text-orange-500';
      case 'MEDIUM': return 'text-yellow-500';
      case 'LOW': return 'text-green-500';
      default: return 'text-gray-500';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'CRITICAL': return <XCircle className="w-4 h-4" />;
      case 'HIGH': return <AlertTriangle className="w-4 h-4" />;
      case 'MEDIUM': return <AlertTriangle className="w-4 h-4" />;
      case 'LOW': return <CheckCircle className="w-4 h-4" />;
      default: return null;
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div className="glass-card w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-tertiary">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-accent-teal to-cyan-500 rounded-lg flex items-center justify-center">
              <Shield className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">Vulnerability Scanner</h2>
              <p className="text-sm text-text-muted">Scan any GitHub repository for security issues</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-text-muted hover:text-text-primary transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* Input Section */}
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">
                GitHub Repository URL
              </label>
              <input
                type="text"
                value={repoUrl}
                onChange={(e) => setRepoUrl(e.target.value)}
                placeholder="https://github.com/username/repository"
                className="w-full px-4 py-3 bg-secondary border border-tertiary rounded-lg focus:outline-none focus:border-accent-teal transition-colors"
                disabled={isScanning}
              />
              <p className="text-xs text-text-muted mt-2">
                Example: https://github.com/deadcoder-n/root
              </p>
            </div>

            {error && (
              <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-lg flex items-start space-x-3">
                <AlertTriangle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-red-500">{error}</p>
              </div>
            )}

            <button
              onClick={handleScan}
              disabled={isScanning}
              className="btn-primary w-full flex items-center justify-center space-x-2"
            >
              {isScanning ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Scanning Repository...</span>
                </>
              ) : (
                <>
                  <Shield className="w-5 h-5" />
                  <span>Start Scan</span>
                </>
              )}
            </button>
          </div>

          {/* Results Section */}
          {scanResult && (
            <div className="space-y-6 animate-fade-in">
              {/* Summary */}
              <div className="glass-card p-6">
                <h3 className="text-xl font-bold mb-4">Scan Summary</h3>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-red-500">
                      {scanResult.severity_breakdown.CRITICAL}
                    </div>
                    <div className="text-xs text-text-muted mt-1">CRITICAL</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-orange-500">
                      {scanResult.severity_breakdown.HIGH}
                    </div>
                    <div className="text-xs text-text-muted mt-1">HIGH</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-yellow-500">
                      {scanResult.severity_breakdown.MEDIUM}
                    </div>
                    <div className="text-xs text-text-muted mt-1">MEDIUM</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-500">
                      {scanResult.severity_breakdown.LOW}
                    </div>
                    <div className="text-xs text-text-muted mt-1">LOW</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold gradient-text">
                      {scanResult.total_vulnerabilities}
                    </div>
                    <div className="text-xs text-text-muted mt-1">TOTAL</div>
                  </div>
                </div>
              </div>

              {/* Vulnerabilities List */}
              <div className="glass-card p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold">Vulnerabilities Found</h3>
                  <div className="flex space-x-2">
                    {scanResult.pdf_available && (
                      <a
                        href={`http://localhost:5000/reports/${encodeURIComponent(scanResult.pdf_report.split('/')[1])}`}
                        download
                        className="btn-primary text-sm flex items-center space-x-2"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <span>Download PDF Report</span>
                      </a>
                    )}
                    <button
                      onClick={() => {
                        const dataStr = JSON.stringify(scanResult, null, 2);
                        const dataBlob = new Blob([dataStr], { type: 'application/json' });
                        const url = URL.createObjectURL(dataBlob);
                        const link = document.createElement('a');
                        link.href = url;
                        link.download = `scan-report-${Date.now()}.json`;
                        link.click();
                        URL.revokeObjectURL(url);
                      }}
                      className="btn-secondary text-sm flex items-center space-x-2"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      <span>Download JSON</span>
                    </button>
                  </div>
                </div>
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {scanResult.vulnerabilities.slice(0, 20).map((vuln, index) => (
                    <div
                      key={index}
                      className="p-4 bg-secondary/50 rounded-lg border border-tertiary hover:border-accent-teal/30 transition-colors"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex items-start space-x-3 flex-1">
                          <div className={getSeverityColor(vuln.severity)}>
                            {getSeverityIcon(vuln.severity)}
                          </div>
                          <div className="flex-1">
                            <div className="flex items-center space-x-2">
                              <span className={`text-sm font-semibold ${getSeverityColor(vuln.severity)}`}>
                                {vuln.severity}
                              </span>
                              <span className="text-xs text-text-muted">•</span>
                              <span className="text-sm font-medium">{vuln.type}</span>
                            </div>
                            <p className="text-xs text-text-muted mt-1">
                              File: {vuln.file}
                            </p>
                            <p className="text-xs text-accent-teal mt-1">
                              {vuln.cwe}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                  {scanResult.vulnerabilities.length > 20 && (
                    <p className="text-sm text-text-muted text-center py-2">
                      ... and {scanResult.vulnerabilities.length - 20} more vulnerabilities
                    </p>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
