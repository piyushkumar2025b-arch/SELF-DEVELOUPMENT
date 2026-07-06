const { useState, useEffect } = React;

function InteractiveDashboard() {
    const [selectedTopic, setSelectedTopic] = useState("Arrays & Hashing");
    const [clickCount, setClickCount] = useState(0);
    const [hoveredCard, setHoveredCard] = useState(null);

    const dsaTopics = {
        "Arrays & Hashing": [
            { id: 1, title: "Two Sum", difficulty: "Easy", company: "Google", link: "https://leetcode.com/problems/two-sum/" },
            { id: 2, title: "Product of Array Except Self", difficulty: "Medium", company: "Facebook", link: "https://leetcode.com/problems/product-of-array-except-self/" },
            { id: 3, title: "Longest Consecutive Sequence", difficulty: "Medium", company: "Google", link: "https://leetcode.com/problems/longest-consecutive-sequence/" }
        ],
        "Two Pointers": [
            { id: 4, title: "Valid Palindrome", difficulty: "Easy", company: "Facebook", link: "https://leetcode.com/problems/valid-palindrome/" },
            { id: 5, title: "3Sum", difficulty: "Medium", company: "Amazon", link: "https://leetcode.com/problems/3sum/" },
            { id: 6, title: "Trapping Rain Water", difficulty: "Hard", company: "Google", link: "https://leetcode.com/problems/trapping-rain-water/" }
        ],
        "Sliding Window": [
            { id: 7, title: "Longest Substring Without Repeating", difficulty: "Medium", company: "Amazon", link: "https://leetcode.com/problems/longest-substring-without-repeating-characters/" },
            { id: 8, title: "Minimum Window Substring", difficulty: "Hard", company: "Facebook", link: "https://leetcode.com/problems/minimum-window-substring/" }
        ]
    };

    const achievements = [
        { icon: "🥷", name: "Code Ninja", color: "#10b981", desc: "Viewed all DSA topics" },
        { icon: "🔥", name: "Week Warrior", color: "#fbbf24", desc: "7-Day Login Streak" },
        { icon: "🔌", name: "API Wizard", color: "#6366f1", desc: "Connected Github, LC, CF" }
    ];

    const handleBadgeClick = (e, color) => {
        const rect = e.currentTarget.getBoundingClientRect();
        const x = rect.left + rect.width / 2;
        const y = rect.top + rect.height / 2;
        if (window.triggerParticles) {
            window.triggerParticles(x, y, color);
        }
        setClickCount(prev => prev + 1);
    };

    return (
        <div className="text-slate-100 p-4 max-w-4xl mx-auto font-sans">
            {/* Header section */}
            <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-slate-800 pb-4 mb-6">
                <div>
                    <h1 className="text-2xl font-extrabold bg-gradient-to-r from-indigo-400 via-purple-400 to-emerald-400 bg-clip-text text-transparent">
                        Interactive Prep Engine
                    </h1>
                    <p className="text-xs text-slate-400 mt-1">Built with React, JSX & Tailwind CSS</p>
                </div>
                <div className="mt-3 md:mt-0 flex gap-2">
                    <button 
                        onClick={() => { if(window.triggerConfetti) window.triggerConfetti(); }}
                        className="px-4 py-1.5 text-xs font-semibold rounded-lg bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 transition shadow-lg shadow-indigo-500/20"
                    >
                        🎉 Launch Celebration
                    </button>
                </div>
            </div>

            {/* Achievement Pins */}
            <div className="mb-6">
                <h3 className="text-sm font-semibold text-slate-400 mb-3">Interactive Achievements (Click to pop)</h3>
                <div className="flex flex-wrap gap-3">
                    {achievements.map((ach, idx) => (
                        <div 
                            key={idx}
                            onClick={(e) => handleBadgeClick(e, ach.color)}
                            className="flex items-center gap-2 bg-slate-900/60 border border-slate-800 px-4 py-2 rounded-xl cursor-pointer hover:border-slate-500 hover:scale-105 active:scale-95 transition-all shadow-sm"
                        >
                            <span className="text-xl">{ach.icon}</span>
                            <div>
                                <div className="text-xs font-bold text-slate-200">{ach.name}</div>
                                <div className="text-[10px] text-slate-400">{ach.desc}</div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Interactive Dropdown Section */}
            <div className="bg-slate-950/80 border border-slate-800 p-5 rounded-2xl shadow-xl backdrop-blur-md">
                <h3 className="text-sm font-bold text-slate-300 mb-4">📚 Curated LeetCode Tracks (Touch Highlight Dropdown)</h3>
                
                <div className="mb-4">
                    <label className="block text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-2">Select DSA Topic</label>
                    <select 
                        value={selectedTopic}
                        onChange={(e) => setSelectedTopic(e.target.value)}
                        className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-2.5 text-slate-200 text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:outline-none transition"
                    >
                        {Object.keys(dsaTopics).map((topic, i) => (
                            <option key={i} value={topic}>{topic}</option>
                        ))}
                    </select>
                </div>

                <div className="space-y-3">
                    {dsaTopics[selectedTopic].map((q) => {
                        const isHovered = hoveredCard === q.id;
                        return (
                            <div 
                                key={q.id}
                                onMouseEnter={() => setHoveredCard(q.id)}
                                onMouseLeave={() => setHoveredCard(null)}
                                className={`flex items-center justify-between p-4 rounded-xl transition-all duration-300 cursor-pointer ${
                                    isHovered 
                                    ? 'bg-slate-900 border border-indigo-500 shadow-md shadow-indigo-500/10 -translate-y-[1px]' 
                                    : 'bg-slate-900/40 border border-slate-800/80'
                                }`}
                            >
                                <div className="flex flex-col gap-1">
                                    <div className="flex items-center gap-2">
                                        <span className="text-sm font-bold text-slate-200">{q.title}</span>
                                        <span className={`text-[9px] px-2 py-0.5 rounded-full font-bold uppercase ${
                                            q.difficulty === 'Easy' ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/20' : 
                                            q.difficulty === 'Medium' ? 'bg-amber-500/15 text-amber-400 border border-amber-500/20' : 
                                            'bg-rose-500/15 text-rose-400 border border-rose-500/20'
                                        }`}>{q.difficulty}</span>
                                    </div>
                                    <div className="text-[10px] text-slate-500">🏢 Tested at: <span className="text-slate-400 font-semibold">{q.company}</span></div>
                                </div>
                                <a 
                                    href={q.link} 
                                    target="_blank"
                                    rel="noreferrer"
                                    className="bg-indigo-600/15 border border-indigo-500/20 text-indigo-400 px-3 py-1.5 rounded-lg text-xs font-semibold hover:bg-indigo-600 hover:text-white transition"
                                >
                                    Solve 🚀
                                </a>
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* Performance Stats component */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
                <div className="bg-slate-900/30 border border-slate-800 p-3 rounded-xl text-center">
                    <div className="text-xl font-extrabold text-indigo-400">{clickCount}</div>
                    <div className="text-[10px] text-slate-500 uppercase font-semibold">Taps Registered</div>
                </div>
                <div className="bg-slate-900/30 border border-slate-800 p-3 rounded-xl text-center">
                    <div className="text-xl font-extrabold text-emerald-400">18</div>
                    <div className="text-[10px] text-slate-500 uppercase font-semibold">Problems Linked</div>
                </div>
                <div className="bg-slate-900/30 border border-slate-800 p-3 rounded-xl text-center">
                    <div className="text-xl font-extrabold text-amber-400">3</div>
                    <div className="text-[10px] text-slate-500 uppercase font-semibold">Integrations Active</div>
                </div>
                <div className="bg-slate-900/30 border border-slate-800 p-3 rounded-xl text-center">
                    <div className="text-xl font-extrabold text-purple-400">C++</div>
                    <div className="text-[10px] text-slate-500 uppercase font-semibold">Analytics active</div>
                </div>
            </div>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('react-root'));
root.render(<InteractiveDashboard />);
