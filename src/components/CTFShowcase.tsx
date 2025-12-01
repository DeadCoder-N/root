import { Trophy, Target, Flag, Star, TrendingUp } from 'lucide-react';
import { useState } from 'react';

export default function CTFShowcase() {
  const [selectedCategory, setSelectedCategory] = useState('all');

  const ctfStats = [
    { icon: Trophy, label: 'CTFs Completed', value: '50+', color: 'from-accent-gold to-yellow-500' },
    { icon: Star, label: 'Rank on TryHackMe', value: 'Top 5%', color: 'from-accent-teal to-cyan-500' },
    { icon: Target, label: 'HackTheBox Rank', value: 'Pro Hacker', color: 'from-accent-purple to-pink-500' },
    { icon: TrendingUp, label: 'Success Rate', value: '85%', color: 'from-accent-green to-emerald-500' },
  ];

  const ctfChallenges = [
    {
      platform: 'TryHackMe',
      name: 'Blue',
      category: 'Windows',
      difficulty: 'Easy',
      points: 100,
      description: 'Exploit Eternal Blue vulnerability on a Windows machine',
      skills: ['Windows', 'Exploitation', 'Metasploit'],
      completed: true,
    },
    {
      platform: 'HackTheBox',
      name: 'Lame',
      category: 'Linux',
      difficulty: 'Easy',
      points: 150,
      description: 'Penetration testing on a vulnerable Linux system',
      skills: ['Linux', 'Enumeration', 'Privilege Escalation'],
      completed: true,
    },
    {
      platform: 'TryHackMe',
      name: 'Kenobi',
      category: 'Linux',
      difficulty: 'Medium',
      points: 200,
      description: 'Exploit ProFTPD vulnerability and escalate privileges',
      skills: ['SMB', 'FTP', 'Path Hijacking'],
      completed: true,
    },
    {
      platform: 'PicoCTF',
      name: 'Web Exploitation',
      category: 'Web',
      difficulty: 'Medium',
      points: 180,
      description: 'SQL injection and XSS challenges',
      skills: ['SQL Injection', 'XSS', 'Web Security'],
      completed: true,
    },
    {
      platform: 'HackTheBox',
      name: 'Blocky',
      category: 'Web',
      difficulty: 'Medium',
      points: 220,
      description: 'WordPress exploitation and reverse engineering',
      skills: ['WordPress', 'Java', 'Reverse Engineering'],
      completed: true,
    },
    {
      platform: 'TryHackMe',
      name: 'Ice',
      category: 'Windows',
      difficulty: 'Medium',
      points: 190,
      description: 'Exploit CVE-2004-1561 on Icecast server',
      skills: ['Windows', 'CVE Exploitation', 'Mimikatz'],
      completed: true,
    },
  ];

  const categories = ['all', 'Web', 'Linux', 'Windows', 'Crypto'];

  const filteredChallenges = selectedCategory === 'all'
    ? ctfChallenges
    : ctfChallenges.filter(c => c.category === selectedCategory);

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Easy':
        return 'text-accent-green bg-accent-green/10 border-accent-green/30';
      case 'Medium':
        return 'text-accent-gold bg-accent-gold/10 border-accent-gold/30';
      case 'Hard':
        return 'text-accent-pink bg-accent-pink/10 border-accent-pink/30';
      default:
        return 'text-accent-teal bg-accent-teal/10 border-accent-teal/30';
    }
  };

  return (
    <section className="py-20 bg-primary">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16 fade-in">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            CTF <span className="gradient-text">Achievements</span>
          </h2>
          <p className="text-text-muted max-w-2xl mx-auto">
            Hands-on experience solving real-world security challenges
          </p>
        </div>

        <div className="grid md:grid-cols-4 gap-6 mb-12">
          {ctfStats.map((stat, index) => (
            <div
              key={index}
              className="glass-card p-6 text-center space-y-4 fade-in"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className={`w-16 h-16 mx-auto bg-gradient-to-r ${stat.color} rounded-full flex items-center justify-center`}>
                <stat.icon className="w-8 h-8 text-white" />
              </div>
              <div>
                <p className="text-3xl font-bold gradient-text">{stat.value}</p>
                <p className="text-text-muted text-sm mt-1">{stat.label}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="mb-8 fade-in">
          <div className="flex flex-wrap justify-center gap-3">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-6 py-2 rounded-lg font-medium transition-all ${
                  selectedCategory === category
                    ? 'bg-gradient-to-r from-accent-teal to-accent-purple text-white'
                    : 'bg-tertiary/50 text-text-secondary hover:bg-tertiary'
                }`}
              >
                {category.charAt(0).toUpperCase() + category.slice(1)}
              </button>
            ))}
          </div>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredChallenges.map((challenge, index) => (
            <div
              key={index}
              className="glass-card p-6 space-y-4 fade-in"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-xs text-accent-teal font-mono">{challenge.platform}</span>
                  <h3 className="text-xl font-bold mt-1">{challenge.name}</h3>
                </div>
                {challenge.completed && (
                  <Flag className="w-5 h-5 text-accent-green fill-current" />
                )}
              </div>

              <p className="text-text-muted text-sm leading-relaxed">
                {challenge.description}
              </p>

              <div className="flex items-center gap-3">
                <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getDifficultyColor(challenge.difficulty)}`}>
                  {challenge.difficulty}
                </span>
                <span className="text-accent-gold font-mono text-sm">{challenge.points} pts</span>
              </div>

              <div className="flex flex-wrap gap-2">
                {challenge.skills.map((skill, i) => (
                  <span key={i} className="skill-badge text-xs">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-12 text-center fade-in">
          <a
            href="https://tryhackme.com"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-primary inline-flex items-center space-x-2"
          >
            <Trophy className="w-5 h-5" />
            <span>View Full Profile</span>
          </a>
        </div>
      </div>
    </section>
  );
}
