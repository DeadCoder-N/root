import { Shield, Terminal, Lock, Search, Activity, Wifi, Code, Key, Globe, Upload, AlertTriangle, Database, Server, Cloud, FileCode, Zap } from 'lucide-react';
import { useState } from 'react';
import CodeAnalyzerModal from './CodeAnalyzerModal';
import SQLInjectionModal from './SQLInjectionModal';
import XSSModal from './XSSModal';
import APISecurityModal from './APISecurityModal';
import JWTAnalyzerModal from './JWTAnalyzerModal';
import AuthenticationModal from './AuthenticationModal';
import OAuthModal from './OAuthModal';
import SessionModal from './SessionModal';
import WebCrawlerModal from './WebCrawlerModal';
import SSLScannerModal from './SSLScannerModal';
import PortScannerModal from './PortScannerModal';
import DNSAnalyzerModal from './DNSAnalyzerModal';
import FileUploadModal from './FileUploadModal';
import CSRFModal from './CSRFModal';
import XXEModal from './XXEModal';
import BusinessLogicModal from './BusinessLogicModal';
import CommandInjectionModal from './CommandInjectionModal';

export default function SecurityTools() {
  const [activeDemo, setActiveDemo] = useState<string | null>(null);
  const [isAnalyzerOpen, setIsAnalyzerOpen] = useState(false);
  const [isSQLInjectionOpen, setIsSQLInjectionOpen] = useState(false);
  const [isXSSOpen, setIsXSSOpen] = useState(false);
  const [isAPISecurityOpen, setIsAPISecurityOpen] = useState(false);
  const [isJWTAnalyzerOpen, setIsJWTAnalyzerOpen] = useState(false);
  const [isAuthenticationOpen, setIsAuthenticationOpen] = useState(false);
  const [isOAuthOpen, setIsOAuthOpen] = useState(false);
  const [isSessionOpen, setIsSessionOpen] = useState(false);
  const [isWebCrawlerOpen, setIsWebCrawlerOpen] = useState(false);
  const [isSSLScannerOpen, setIsSSLScannerOpen] = useState(false);
  const [isPortScannerOpen, setIsPortScannerOpen] = useState(false);
  const [isDNSAnalyzerOpen, setIsDNSAnalyzerOpen] = useState(false);
  const [isFileUploadOpen, setIsFileUploadOpen] = useState(false);
  const [isCSRFOpen, setIsCSRFOpen] = useState(false);
  const [isXXEOpen, setIsXXEOpen] = useState(false);
  const [isBusinessLogicOpen, setIsBusinessLogicOpen] = useState(false);
  const [isCommandInjectionOpen, setIsCommandInjectionOpen] = useState(false);

  const tools = [
    // ============================================
    // EXISTING TOOLS (1-3) - Keep as is
    // ============================================
    {
      id: 'code-analyzer',
      icon: Code,
      name: 'Vulnerability Scanner',
      category: 'SAST Tool',
      description: 'Production-grade security scanner. Detects secrets, vulnerabilities, outdated dependencies in GitHub repos',
      color: 'from-accent-teal to-cyan-500',
      isLive: true,
      port: 5001,
    },
    {
      id: 'sql-injection',
      icon: Lock,
      name: 'SQL Injection Tester',
      category: 'Web Security',
      description: 'Production-grade SQL injection scanner. Tests for error-based, union-based, and time-based SQLi',
      color: 'from-accent-purple to-pink-500',
      isLive: true,
      port: 5002,
    },
    {
      id: 'xss-detector',
      icon: Terminal,
      name: 'XSS Scanner',
      category: 'Web Security',
      description: 'Production-grade XSS scanner. Detects reflected, stored, and DOM-based Cross-Site Scripting',
      color: 'from-accent-gold to-yellow-500',
      isLive: true,
      port: 5003,
    },
    
    // ============================================
    // NEW TOOLS (4-17) - Added systematically
    // ============================================
    {
      id: 'api-security',
      icon: Database,
      name: 'API Security Tester',
      category: 'API Security',
      description: 'Test APIs for BOLA, authentication, mass assignment, rate limiting, and OWASP API Top 10',
      color: 'from-blue-500 to-indigo-500',
      isLive: true,
      port: 5004,
    },
    {
      id: 'jwt-analyzer',
      icon: Key,
      name: 'JWT Analyzer',
      category: 'Authentication',
      description: 'Analyze JWT tokens for algorithm none attack, weak secrets, expiration, and signature validation',
      color: 'from-purple-500 to-pink-500',
      isLive: true,
      port: 5005,
    },
    {
      id: 'auth-analyzer',
      icon: Shield,
      name: 'Authentication Analyzer',
      category: 'Authentication',
      description: 'Test authentication mechanisms for brute force, password policy, session management, and 2FA',
      color: 'from-red-500 to-orange-500',
      isLive: true,
      port: 5006,
    },
    {
      id: 'oauth-tester',
      icon: Lock,
      name: 'OAuth Security Tester',
      category: 'Authentication',
      description: 'Test OAuth flows for state parameter, redirect URI, PKCE, code injection, and token leakage',
      color: 'from-green-500 to-teal-500',
      isLive: true,
      port: 5007,
    },
    {
      id: 'session-analyzer',
      icon: Activity,
      name: 'Session Analyzer',
      category: 'Web Security',
      description: 'Analyze session management for fixation, CSRF, cookie security, and timeout issues',
      color: 'from-yellow-500 to-amber-500',
      isLive: true,
      port: 5008,
    },
    {
      id: 'web-crawler',
      icon: Globe,
      name: 'Web Crawler',
      category: 'Reconnaissance',
      description: 'Crawl websites to map endpoints, extract links, detect forms, clickjacking, and open redirects',
      color: 'from-cyan-500 to-blue-500',
      isLive: true,
      port: 5009,
    },
    {
      id: 'ssl-scanner',
      icon: Lock,
      name: 'SSL/TLS Scanner',
      category: 'Network Security',
      description: 'Scan SSL/TLS configurations for certificate validation, weak protocols, and cipher suites',
      color: 'from-indigo-500 to-purple-500',
      isLive: true,
      port: 5010,
    },
    {
      id: 'port-scanner',
      icon: Search,
      name: 'Port Scanner',
      category: 'Reconnaissance',
      description: 'Scan network ports for open services, banner grabbing, and service detection',
      color: 'from-pink-500 to-rose-500',
      isLive: true,
      port: 5011,
    },
    {
      id: 'dns-analyzer',
      icon: Server,
      name: 'DNS Analyzer',
      category: 'Network Security',
      description: 'Analyze DNS records, DNSSEC, SPF, DMARC, and zone transfer vulnerabilities',
      color: 'from-teal-500 to-green-500',
      isLive: true,
      port: 5012,
    },
    {
      id: 'file-upload',
      icon: Upload,
      name: 'File Upload Tester',
      category: 'Web Security',
      description: 'Test file upload functionality for extension validation, MIME type, size limits, and path traversal',
      color: 'from-orange-500 to-red-500',
      isLive: true,
      port: 5013,
    },
    {
      id: 'csrf-tester',
      icon: AlertTriangle,
      name: 'CSRF Tester',
      category: 'Web Security',
      description: 'Test for CSRF vulnerabilities, token validation, SameSite cookies, and CORS policy',
      color: 'from-red-500 to-pink-500',
      isLive: true,
      port: 5014,
    },
    {
      id: 'xxe-scanner',
      icon: FileCode,
      name: 'XXE Scanner',
      category: 'Web Security',
      description: 'Scan for XML External Entity vulnerabilities, file reading, XML bomb, and SSRF via XXE',
      color: 'from-purple-500 to-indigo-500',
      isLive: true,
      port: 5015,
    },
    {
      id: 'business-logic',
      icon: Zap,
      name: 'Business Logic Tester',
      category: 'Application Security',
      description: 'Test business logic for race conditions, price manipulation, negative values, and parameter tampering',
      color: 'from-yellow-500 to-orange-500',
      isLive: true,
      port: 5016,
    },
    {
      id: 'command-injection',
      icon: Terminal,
      name: 'Command Injection Scanner',
      category: 'Web Security',
      description: 'Scan for OS command injection, path traversal, and local file inclusion vulnerabilities',
      color: 'from-red-500 to-rose-500',
      isLive: true,
      port: 5017,
    },
  ];

  return (
    <section className="py-20 bg-primary">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16 fade-in">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Security <span className="gradient-text">Tools Suite</span>
          </h2>
          <p className="text-text-muted max-w-2xl mx-auto">
            Professional-grade cybersecurity testing toolkit with 17 specialized tools
          </p>
          <div className="mt-4 flex justify-center gap-4 text-sm">
            <span className="px-4 py-2 bg-accent-teal/10 border border-accent-teal/30 rounded-full text-accent-teal">
              17 Tools Available
            </span>
            <span className="px-4 py-2 bg-accent-purple/10 border border-accent-purple/30 rounded-full text-accent-purple">
              59+ Features
            </span>
            <span className="px-4 py-2 bg-accent-gold/10 border border-accent-gold/30 rounded-full text-accent-gold">
              Production Ready
            </span>
          </div>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tools.map((tool, index) => (
            <div
              key={tool.id}
              className="glass-card p-6 space-y-4 cursor-pointer fade-in hover:scale-105 transition-transform"
              style={{ animationDelay: `${index * 0.05}s` }}
              onClick={() => setActiveDemo(activeDemo === tool.id ? null : tool.id)}
            >
              <div className="flex items-start justify-between">
                <div className={`w-12 h-12 bg-gradient-to-r ${tool.color} rounded-lg flex items-center justify-center flex-shrink-0`}>
                  <tool.icon className="w-6 h-6 text-white" />
                </div>
                <span className="text-xs text-accent-teal font-mono px-3 py-1 bg-accent-teal/10 rounded-full border border-accent-teal/30">
                  {tool.category}
                </span>
              </div>

              <div>
                <h3 className="text-xl font-bold mb-2">{tool.name}</h3>
                <p className="text-text-muted text-sm leading-relaxed">
                  {tool.description}
                </p>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-xs text-text-muted font-mono">
                  Port: {tool.port}
                </span>
                <span className="text-xs px-2 py-1 bg-green-500/10 border border-green-500/30 rounded text-green-500">
                  ● Live
                </span>
              </div>

              <button
                onClick={(e) => {
                  if (tool.isLive) {
                    e.stopPropagation();
                    if (tool.id === 'code-analyzer') setIsAnalyzerOpen(true);
                    else if (tool.id === 'sql-injection') setIsSQLInjectionOpen(true);
                    else if (tool.id === 'xss-detector') setIsXSSOpen(true);
                    else if (tool.id === 'api-security') setIsAPISecurityOpen(true);
                    else if (tool.id === 'jwt-analyzer') setIsJWTAnalyzerOpen(true);
                    else if (tool.id === 'auth-analyzer') setIsAuthenticationOpen(true);
                    else if (tool.id === 'oauth-tester') setIsOAuthOpen(true);
                    else if (tool.id === 'session-analyzer') setIsSessionOpen(true);
                    else if (tool.id === 'web-crawler') setIsWebCrawlerOpen(true);
                    else if (tool.id === 'ssl-scanner') setIsSSLScannerOpen(true);
                    else if (tool.id === 'port-scanner') setIsPortScannerOpen(true);
                    else if (tool.id === 'dns-analyzer') setIsDNSAnalyzerOpen(true);
                    else if (tool.id === 'file-upload') setIsFileUploadOpen(true);
                    else if (tool.id === 'csrf-tester') setIsCSRFOpen(true);
                    else if (tool.id === 'xxe-scanner') setIsXXEOpen(true);
                    else if (tool.id === 'business-logic') setIsBusinessLogicOpen(true);
                    else if (tool.id === 'command-injection') setIsCommandInjectionOpen(true);
                  }
                }}
                className={`w-full py-2 rounded-lg font-medium text-sm transition-all ${
                  tool.isLive
                    ? 'bg-gradient-to-r from-accent-teal to-accent-purple text-white hover:shadow-lg hover:shadow-accent-teal/50'
                    : 'bg-tertiary text-text-secondary hover:bg-tertiary/80'
                }`}
              >
                {tool.isLive ? '🚀 Launch Tool' : 'Coming Soon'}
              </button>
            </div>
          ))}
        </div>

        <div className="mt-12 text-center">
          <p className="text-text-muted text-sm">
            All tools are production-ready with comprehensive error handling, PDF reports, and fix prompts
          </p>
        </div>
      </div>
      
      <CodeAnalyzerModal isOpen={isAnalyzerOpen} onClose={() => setIsAnalyzerOpen(false)} />
      <SQLInjectionModal isOpen={isSQLInjectionOpen} onClose={() => setIsSQLInjectionOpen(false)} />
      <XSSModal isOpen={isXSSOpen} onClose={() => setIsXSSOpen(false)} />
      <APISecurityModal isOpen={isAPISecurityOpen} onClose={() => setIsAPISecurityOpen(false)} />
      <JWTAnalyzerModal isOpen={isJWTAnalyzerOpen} onClose={() => setIsJWTAnalyzerOpen(false)} />
      <AuthenticationModal isOpen={isAuthenticationOpen} onClose={() => setIsAuthenticationOpen(false)} />
      <OAuthModal isOpen={isOAuthOpen} onClose={() => setIsOAuthOpen(false)} />
      <SessionModal isOpen={isSessionOpen} onClose={() => setIsSessionOpen(false)} />
      <WebCrawlerModal isOpen={isWebCrawlerOpen} onClose={() => setIsWebCrawlerOpen(false)} />
      <SSLScannerModal isOpen={isSSLScannerOpen} onClose={() => setIsSSLScannerOpen(false)} />
      <PortScannerModal isOpen={isPortScannerOpen} onClose={() => setIsPortScannerOpen(false)} />
      <DNSAnalyzerModal isOpen={isDNSAnalyzerOpen} onClose={() => setIsDNSAnalyzerOpen(false)} />
      <FileUploadModal isOpen={isFileUploadOpen} onClose={() => setIsFileUploadOpen(false)} />
      <CSRFModal isOpen={isCSRFOpen} onClose={() => setIsCSRFOpen(false)} />
      <XXEModal isOpen={isXXEOpen} onClose={() => setIsXXEOpen(false)} />
      <BusinessLogicModal isOpen={isBusinessLogicOpen} onClose={() => setIsBusinessLogicOpen(false)} />
      <CommandInjectionModal isOpen={isCommandInjectionOpen} onClose={() => setIsCommandInjectionOpen(false)} />
    </section>
  );
}
