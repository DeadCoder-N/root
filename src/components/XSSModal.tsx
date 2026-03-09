import React, { useState } from 'react';
import { X, Shield, AlertTriangle, Download, FileJson, Loader2, Zap, Terminal } from 'lucide-react';

interface Vulnerability {
  parameter: string;
  type: string;
  severity: string;
  payload: string;
  evidence: string;
  url: string;
}

interface XSSModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function XSSModal({ isOpen, onClose }: XSSModalProps) {
  const [url, setUrl] = useState('');
  const [isScanning, setIsScanning] = useState(false);
  const [scanComplete, setScanComplete] = useState(false);
  const [vulnerabilities, setVulnerabilities] = useState<Vulnerability[]>([]);
  const [scanId, setScanId] = useState('');
  const [progress, setProgress] = useState({ message: '', percentage: 0 });
  const [error, setError] = useState('');

  const handleScan = async () => {
    if (!url.trim()) {
      setError('Please enter a URL');
      return;
    }

    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      setError('URL must start with http:// or https://');
      return;
    }

    setIsScanning(true);
    setScanComplete(false);
    setError('');
    setVulnerabilities([]);
    setProgress({ message: 'Starting scan...', percentage: 0 });

    try {
      const response = await fetch('http://localhost:5003/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });

      const data = await response.json();

      if (response.ok) {
        setVulnerabilities(data.vulnerabilities || []);
        setScanId(data.scan_id);
        setScanComplete(true);
        setProgress({ message: 'Scan complete!', percentage: 100 });
      } else {
        setError(data.error || 'Scan failed');
      }
    } catch (err) {
      setError('Failed to connect to XSS Scanner backend. Make sure it\'s running on port 5003.');
    } finally {
      setIsScanning(false);
    }
  };

  const handleDownloadPDF = async () => {
    try {
      const response = await fetch(`http://localhost:5003/api/download/${scanId}`);
      
      if (response.ok) {
        const blob = await response.blob();
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = 'xss_report.pdf';
        
        if (contentDisposition) {
          const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition);
          if (matches && matches[1]) {
            filename = matches[1].replace(/['"]/g, '');
          }
        }
        
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        document.body.removeChild(a);
      }
    } catch (err) {
      setError('Failed to download PDF report');
    }
  };

  const handleDownloadJSON = () => {
    const jsonData = JSON.stringify({ url, vulnerabilities }, null, 2);
    const blob = new Blob([jsonData], { type: 'application/json' });
    const downloadUrl = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = `xss_scan_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(downloadUrl);
    document.body.removeChild(a);
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'CRITICAL': return 'text-red-600 bg-red-50 border-red-200';
      case 'HIGH': return 'text-orange-600 bg-orange-50 border-orange-200';
      case 'MEDIUM': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      default: return 'text-blue-600 bg-blue-50 border-blue-200';
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div className="bg-secondary border border-accent-teal/30 rounded-2xl w-full max-w-6xl max-h-[90vh] overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="bg-gradient-to-r from-accent-teal/20 to-accent-purple/20 border-b border-accent-teal/30 p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-r from-accent-teal to-accent-purple rounded-lg flex items-center justify-center">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold gradient-text">XSS Scanner</h2>
                <p className="text-sm text-text-muted font-mono">Cross-Site Scripting Detector</p>
              </div>
            </div>
            <button onClick={onClose} className="w-10 h-10 rounded-lg bg-tertiary hover:bg-tertiary/80 transition-colors flex items-center justify-center">
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
          {/* Input Section */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-accent-teal mb-2">
              <Zap className="w-4 h-4 inline mr-2" />Target URL
            </label>
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com/search?q=test"
              className="w-full px-4 py-3 bg-tertiary border border-accent-teal/30 rounded-lg focus:outline-none focus:border-accent-teal text-text-primary placeholder-text-muted font-mono text-sm"
              disabled={isScanning}
            />
            <p className="text-xs text-text-muted mt-2">
              <Terminal className="w-3 h-3 inline mr-1" />
              Enter a URL with query parameters (e.g., ?q=test, ?search=value)
            </p>
          </div>

          {/* Scan Button */}
          <div className="flex items-center justify-end">
            <button
              onClick={handleScan}
              disabled={isScanning}
              className="px-8 py-3 bg-gradient-to-r from-accent-teal to-accent-purple text-white rounded-lg font-semibold hover:shadow-lg hover:shadow-accent-teal/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed mt-7 flex items-center justify-center gap-2"
            >
              {isScanning ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Scanning...
                </>
              ) : (
                <>
                  <Shield className="w-5 h-5" />
                  Start XSS Scan
                </>
              )}
            </button>
          </div>

          {/* Progress */}
          {isScanning && (
            <div className="mt-4 bg-accent-teal/10 border border-accent-teal/30 rounded-lg p-6">
              <div className="flex items-center justify-between mb-3">
                <p className="text-accent-teal font-semibold">{progress.message}</p>
                <p className="text-accent-teal font-mono text-sm">{progress.percentage}%</p>
              </div>
              <div className="w-full bg-tertiary rounded-full h-2 overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-accent-teal to-accent-purple transition-all duration-500"
                  style={{ width: `${progress.percentage}%` }}
                />
              </div>
            </div>
          )}

          {/* Error */}
          {error && (
            <div className="mt-4 bg-red-500/10 border border-red-500/30 rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <AlertTriangle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="text-red-500 font-semibold mb-1">Error</p>
                  <p className="text-sm text-text-muted font-mono">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Results */}
          {scanComplete && (
            <div className="mt-6 space-y-4">
              {/* Summary */}
              <div className="bg-gradient-to-r from-accent-teal/10 to-accent-purple/10 p-4 rounded-lg border border-accent-teal/30">
                <h3 className="font-semibold text-accent-teal mb-2">Scan Summary</h3>
                <p className="text-sm text-text-muted">
                  Found <span className="font-bold text-accent-teal">{vulnerabilities.length}</span> XSS vulnerabilities
                </p>
              </div>

              {/* Vulnerabilities */}
              {vulnerabilities.length > 0 ? (
                <div className="space-y-3">
                  {vulnerabilities.map((vuln, index) => (
                    <div
                      key={index}
                      className={`p-4 rounded-lg border ${getSeverityColor(vuln.severity)}`}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <span className="font-semibold">{vuln.type}</span>
                          <span className="ml-2 text-xs px-2 py-1 rounded bg-white/50">
                            {vuln.severity}
                          </span>
                        </div>
                      </div>
                      <div className="text-sm space-y-1">
                        <p><span className="font-medium">Parameter:</span> {vuln.parameter}</p>
                        <p><span className="font-medium">Payload:</span> <code className="bg-white/50 px-1 rounded">{vuln.payload}</code></p>
                        <p><span className="font-medium">Evidence:</span> {vuln.evidence}</p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 bg-green-500/10 border border-green-500/30 rounded-lg">
                  <Shield className="w-12 h-12 text-green-500 mx-auto mb-3" />
                  <p className="text-green-500 font-semibold">No XSS vulnerabilities found!</p>
                  <p className="text-sm text-text-muted mt-1">Your application appears secure</p>
                </div>
              )}

              {/* Download Buttons */}
              {vulnerabilities.length > 0 && (
                <div className="flex gap-3">
                  <button
                    onClick={handleDownloadPDF}
                    className="flex-1 bg-gradient-to-r from-accent-teal to-accent-purple text-white py-2 rounded-lg font-semibold hover:shadow-lg transition-all flex items-center justify-center gap-2"
                  >
                    <Download className="w-4 h-4" />
                    Download PDF Report
                  </button>
                  <button
                    onClick={handleDownloadJSON}
                    className="flex-1 bg-tertiary hover:bg-tertiary/80 text-text-primary py-2 rounded-lg font-semibold transition-colors flex items-center justify-center gap-2"
                  >
                    <FileJson className="w-4 h-4" />
                    Download JSON
                  </button>
                </div>
              )}
            </div>
          )}

          {/* Empty State */}
          {!isScanning && !scanComplete && !error && (
            <div className="text-center py-12">
              <Shield className="w-16 h-16 mx-auto mb-4 text-accent-teal" />
              <p className="text-lg font-medium text-text-primary">Ready to scan for XSS vulnerabilities</p>
              <p className="text-sm mt-2 text-text-muted">Enter a URL and click "Start XSS Scan"</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
