import { Shield, Terminal, Lock, Search, Activity, Wifi } from 'lucide-react';
import { useState } from 'react';

export default function SecurityTools() {
  const [activeDemo, setActiveDemo] = useState<string | null>(null);

  const tools = [
    {
      id: 'port-scanner',
      icon: Search,
      name: 'Port Scanner',
      category: 'Reconnaissance',
      description: 'Simulate network port scanning to identify open ports and services',
      color: 'from-accent-teal to-cyan-500',
      demo: {
        title: 'Nmap Scan Simulation',
        code: `nmap -sV -sC 192.168.1.1

Starting Nmap scan...
PORT     STATE  SERVICE     VERSION
22/tcp   open   ssh         OpenSSH 8.2
80/tcp   open   http        Apache 2.4.41
443/tcp  open   ssl/https   Apache 2.4.41
3306/tcp closed mysql

Scan complete. 3 open ports found.`,
      },
    },
    {
      id: 'sql-injection',
      icon: Lock,
      name: 'SQL Injection Tester',
      category: 'Web Security',
      description: 'Demonstrate SQL injection vulnerabilities and prevention techniques',
      color: 'from-accent-purple to-pink-500',
      demo: {
        title: 'SQL Injection Detection',
        code: `Testing payload: admin' OR '1'='1

[!] Vulnerability detected!
Input: admin' OR '1'='1
Query: SELECT * FROM users WHERE username='admin' OR '1'='1'
Status: VULNERABLE

Fix: Use parameterized queries
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
$stmt->execute([$username]);`,
      },
    },
    {
      id: 'password-hash',
      icon: Shield,
      name: 'Password Hasher',
      category: 'Cryptography',
      description: 'Hash passwords using various algorithms (MD5, SHA256, bcrypt)',
      color: 'from-accent-pink to-red-500',
      demo: {
        title: 'Password Hashing',
        code: `Input: MySecurePass123

MD5:     5f4dcc3b5aa765d61d8327deb882cf99
SHA256:  a665a45920422f9d417e4867efdc4fb8a0
bcrypt:  $2b$10$N9qo8uLOickgx2ZMRZoMy.

Recommendation: Use bcrypt or Argon2
Time to crack MD5:     < 1 second
Time to crack bcrypt:  Years`,
      },
    },
    {
      id: 'xss-detector',
      icon: Terminal,
      name: 'XSS Vulnerability Scanner',
      category: 'Web Security',
      description: 'Detect Cross-Site Scripting vulnerabilities in web applications',
      color: 'from-accent-gold to-yellow-500',
      demo: {
        title: 'XSS Detection',
        code: `Testing payload: <script>alert('XSS')</script>

[!] XSS Vulnerability Found!
Type: Reflected XSS
Location: search parameter
Risk: HIGH

Remediation:
1. Sanitize user input
2. Encode output
3. Use Content Security Policy
4. Validate on server-side`,
      },
    },
    {
      id: 'network-sniffer',
      icon: Activity,
      name: 'Packet Analyzer',
      category: 'Network Security',
      description: 'Capture and analyze network packets in real-time',
      color: 'from-accent-green to-emerald-500',
      demo: {
        title: 'Packet Capture',
        code: `Capturing packets on eth0...

Frame 1: HTTP Request
Source: 192.168.1.100
Dest: 93.184.216.34
Protocol: HTTP/1.1
GET /index.html HTTP/1.1

Frame 2: TCP Handshake
SYN -> SYN-ACK -> ACK
Connection established

Total packets captured: 1,247`,
      },
    },
    {
      id: 'wifi-audit',
      icon: Wifi,
      name: 'WiFi Security Auditor',
      category: 'Wireless Security',
      description: 'Audit wireless networks for security vulnerabilities',
      color: 'from-blue-500 to-cyan-500',
      demo: {
        title: 'WiFi Security Audit',
        code: `Scanning wireless networks...

SSID: HomeNetwork
BSSID: 00:11:22:33:44:55
Security: WPA2-PSK
Signal: -45 dBm
Status: SECURE

SSID: GuestWiFi
Security: WEP
Status: VULNERABLE (Weak encryption)

Recommendation: Upgrade to WPA3`,
      },
    },
  ];

  return (
    <section className="py-20 bg-primary">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16 fade-in">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Security <span className="gradient-text">Tools Demo</span>
          </h2>
          <p className="text-text-muted max-w-2xl mx-auto">
            Interactive demonstrations of common cybersecurity tools and techniques
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tools.map((tool, index) => (
            <div
              key={tool.id}
              className="glass-card p-6 space-y-4 cursor-pointer fade-in"
              style={{ animationDelay: `${index * 0.1}s` }}
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

              <button
                className={`w-full py-2 rounded-lg font-medium text-sm transition-all ${
                  activeDemo === tool.id
                    ? 'bg-gradient-to-r from-accent-teal to-accent-purple text-white'
                    : 'bg-tertiary text-text-secondary hover:bg-tertiary/80'
                }`}
              >
                {activeDemo === tool.id ? 'Hide Demo' : 'View Demo'}
              </button>

              {activeDemo === tool.id && (
                <div className="mt-4 bg-primary border border-accent-teal/30 rounded-lg overflow-hidden">
                  <div className="bg-tertiary px-4 py-2 border-b border-accent-teal/30">
                    <p className="text-sm font-semibold text-accent-teal">{tool.demo.title}</p>
                  </div>
                  <pre className="p-4 text-xs font-mono text-text-secondary overflow-x-auto whitespace-pre-wrap leading-relaxed">
                    {tool.demo.code}
                  </pre>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="mt-16 text-center fade-in">
          <div className="glass-card p-8 max-w-3xl mx-auto">
            <h3 className="text-2xl font-bold mb-4">Educational Purpose Only</h3>
            <p className="text-text-muted leading-relaxed">
              These demonstrations are for educational purposes to showcase understanding of cybersecurity concepts.
              All tools and techniques should only be used on systems you own or have explicit permission to test.
              Unauthorized access to computer systems is illegal and unethical.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
