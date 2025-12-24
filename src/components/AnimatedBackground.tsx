export default function AnimatedBackground() {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
      {/* Animated Grid */}
      <div 
        className="absolute inset-0 opacity-5"
        style={{
          backgroundImage: `
            linear-gradient(rgba(6, 182, 212, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(6, 182, 212, 0.1) 1px, transparent 1px)
          `,
          backgroundSize: '50px 50px',
          animation: 'gridMove 20s linear infinite'
        }}
      />
      
      {/* Moving Gradient Orbs */}
      <div className="absolute inset-0">
        <div 
          className="absolute w-96 h-96 rounded-full opacity-10"
          style={{
            background: 'radial-gradient(circle, #06b6d4 0%, transparent 70%)',
            animation: 'floatOrb1 15s ease-in-out infinite',
            top: '10%',
            left: '10%'
          }}
        />
        <div 
          className="absolute w-80 h-80 rounded-full opacity-10"
          style={{
            background: 'radial-gradient(circle, #7c3aed 0%, transparent 70%)',
            animation: 'floatOrb2 18s ease-in-out infinite',
            bottom: '20%',
            right: '15%'
          }}
        />
        <div 
          className="absolute w-64 h-64 rounded-full opacity-10"
          style={{
            background: 'radial-gradient(circle, #ec4899 0%, transparent 70%)',
            animation: 'floatOrb3 12s ease-in-out infinite',
            top: '50%',
            left: '50%'
          }}
        />
      </div>
    </div>
  );
}