import { Shield, Code, Database, Terminal, Globe, Lock } from 'lucide-react';

export default function Skills() {
  const skillCategories = [
    {
      icon: Shield,
      title: 'Cybersecurity',
      color: 'from-accent-teal to-cyan-500',
      skills: [
        { name: 'Penetration Testing', level: 85 },
        { name: 'VAPT', level: 80 },
        { name: 'Burp Suite', level: 85 },
        { name: 'Metasploit', level: 75 },
        { name: 'Nessus', level: 70 },
        { name: 'Wireshark', level: 80 },
        { name: 'OWASP Top 10', level: 90 },
        { name: 'Ethical Hacking', level: 85 },
      ],
    },
    {
      icon: Code,
      title: 'Frontend Development',
      color: 'from-accent-purple to-pink-500',
      skills: [
        { name: 'React.js', level: 90 },
        { name: 'JavaScript/TypeScript', level: 85 },
        { name: 'HTML5/CSS3', level: 95 },
        { name: 'Tailwind CSS', level: 90 },
        { name: 'Next.js', level: 75 },
        { name: 'Redux', level: 70 },
        { name: 'REST APIs', level: 85 },
        { name: 'Git/GitHub', level: 85 },
      ],
    },
    {
      icon: Database,
      title: 'Backend & Databases',
      color: 'from-accent-pink to-red-500',
      skills: [
        { name: 'Node.js', level: 75 },
        { name: 'Express.js', level: 70 },
        { name: 'MongoDB', level: 75 },
        { name: 'PostgreSQL', level: 70 },
        { name: 'Supabase', level: 80 },
        { name: 'Firebase', level: 75 },
      ],
    },
    {
      icon: Terminal,
      title: 'Programming & Scripting',
      color: 'from-accent-gold to-yellow-500',
      skills: [
        { name: 'Python', level: 85 },
        { name: 'Bash Scripting', level: 80 },
        { name: 'PowerShell', level: 65 },
        { name: 'SQL', level: 75 },
        { name: 'PHP', level: 60 },
      ],
    },
    {
      icon: Globe,
      title: 'Network Security',
      color: 'from-accent-green to-emerald-500',
      skills: [
        { name: 'Network Analysis', level: 80 },
        { name: 'TCP/IP', level: 85 },
        { name: 'Firewall Configuration', level: 75 },
        { name: 'VPN Setup', level: 70 },
        { name: 'IDS/IPS', level: 75 },
      ],
    },
    {
      icon: Lock,
      title: 'Security Tools',
      color: 'from-blue-500 to-cyan-500',
      skills: [
        { name: 'Nmap', level: 85 },
        { name: 'John the Ripper', level: 75 },
        { name: 'Hashcat', level: 70 },
        { name: 'SQLMap', level: 80 },
        { name: 'Nikto', level: 75 },
        { name: 'Aircrack-ng', level: 70 },
      ],
    },
  ];

  return (
    <section id="skills" className="py-20 bg-primary">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16 fade-in">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Skills & <span className="gradient-text">Expertise</span>
          </h2>
          <p className="text-text-muted max-w-2xl mx-auto">
            A comprehensive toolkit combining cybersecurity and development skills
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {skillCategories.map((category, index) => (
            <div
              key={index}
              className="glass-card p-6 space-y-6 fade-in"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="flex items-center space-x-4">
                <div className={`w-12 h-12 bg-gradient-to-r ${category.color} rounded-lg flex items-center justify-center`}>
                  <category.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold">{category.title}</h3>
              </div>

              <div className="space-y-4">
                {category.skills.map((skill, skillIndex) => (
                  <div key={skillIndex} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-text-secondary">{skill.name}</span>
                      <span className="text-accent-teal font-mono">{skill.level}%</span>
                    </div>
                    <div className="h-2 bg-tertiary rounded-full overflow-hidden">
                      <div
                        className={`h-full bg-gradient-to-r ${category.color} rounded-full transition-all duration-1000 ease-out`}
                        style={{ width: `${skill.level}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-16 text-center fade-in">
          <h3 className="text-2xl font-semibold mb-8">Certifications & Achievements</h3>
          <div className="flex flex-wrap justify-center gap-4">
            {[
              'CompTIA Security+',
              'CEH (In Progress)',
              'Google Cybersecurity',
              'AWS Cloud Practitioner',
              'TryHackMe Top 5%',
              'HackTheBox Pro Hacker',
              'React Advanced',
              'Node.js Developer',
            ].map((cert, index) => (
              <span key={index} className="skill-badge">
                {cert}
              </span>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
