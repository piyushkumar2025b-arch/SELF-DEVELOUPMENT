const { useState } = React;

function AlgorithmVisualizer() {
    const [activeTab, setActiveTab] = useState("stack");

    // Stack State
    const [stack, setStack] = useState([15, 42, 8]);
    const [stackLog, setStackLog] = useState(["Initial stack values loaded."]);

    // Binary Search State
    const [array] = useState([12, 24, 35, 47, 58, 69, 80, 92, 105, 120]);
    const [target, setTarget] = useState(80);
    const [bsState, setBsState] = useState({
        left: 0,
        right: 9,
        mid: -1,
        step: 0,
        found: false,
        finished: false,
        msg: "Set target and click 'Next Step' to start."
    });

    // Stack Actions
    const handlePush = () => {
        if (stack.length >= 8) {
            setStackLog(prev => ["Stack Overflow! Limit is 8 items.", ...prev]);
            return;
        }
        const val = Math.floor(Math.random() * 90) + 10;
        setStack(prev => [...prev, val]);
        setStackLog(prev => [`Pushed ${val} onto the stack.`, ...prev]);
        if (window.triggerParticles) {
            window.triggerParticles(window.innerWidth / 2, window.innerHeight / 2, "#10b981");
        }
    };

    const handlePop = () => {
        if (stack.length === 0) {
            setStackLog(prev => ["Stack Underflow! Stack is empty.", ...prev]);
            return;
        }
        const popped = stack[stack.length - 1];
        setStack(prev => prev.slice(0, -1));
        setStackLog(prev => [`Popped ${popped} from the stack.`, ...prev]);
        if (window.triggerParticles) {
            window.triggerParticles(window.innerWidth / 2, window.innerHeight / 2, "#ef4444");
        }
    };

    // Binary Search Actions
    const resetBS = (newTarget = target) => {
        setBsState({
            left: 0,
            right: array.length - 1,
            mid: -1,
            step: 0,
            found: false,
            finished: false,
            msg: `Search started for target ${newTarget}.`
        });
    };

    const stepBS = () => {
        if (bsState.finished) return;

        const { left, right, step } = bsState;
        if (left > right) {
            setBsState(prev => ({
                ...prev,
                finished: true,
                msg: `Target ${target} not found in the array.`
            }));
            return;
        }

        const mid = Math.floor((left + right) / 2);
        const val = array[mid];

        if (val === target) {
            setBsState({
                left,
                right,
                mid,
                step: step + 1,
                found: true,
                finished: true,
                msg: `Found target ${target} at index ${mid}! 🎉`
            });
            if (window.triggerConfetti) window.triggerConfetti();
        } else if (val < target) {
            setBsState({
                left: mid + 1,
                right,
                mid,
                step: step + 1,
                found: false,
                finished: false,
                msg: `${val} < ${target}. Search right half (index ${mid + 1} to ${right}).`
            });
        } else {
            setBsState({
                left,
                right: mid - 1,
                mid,
                step: step + 1,
                found: false,
                finished: false,
                msg: `${val} > ${target}. Search left half (index ${left} to ${mid - 1}).`
            });
        }
    };

    return (
        <div className="text-slate-100 p-4 max-w-4xl mx-auto font-sans">
            {/* Visualizer Tabs */}
            <div className="flex gap-2 border-b border-slate-800 pb-3 mb-6">
                <button
                    onClick={() => setActiveTab("stack")}
                    className={`px-4 py-2 text-xs font-bold rounded-lg transition ${
                        activeTab === "stack" ? "bg-indigo-600 text-white" : "bg-slate-900 text-slate-400 hover:text-slate-200"
                    }`}
                >
                    📚 Stack Visualizer (LIFO)
                </button>
                <button
                    onClick={() => setActiveTab("binary")}
                    className={`px-4 py-2 text-xs font-bold rounded-lg transition ${
                        activeTab === "binary" ? "bg-indigo-600 text-white" : "bg-slate-900 text-slate-400 hover:text-slate-200"
                    }`}
                >
                    🔍 Binary Search (Divide & Conquer)
                </button>
            </div>

            {/* Stack Visualizer Panel */}
            {activeTab === "stack" && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-slate-950/80 border border-slate-800 p-5 rounded-2xl shadow-xl">
                    <div>
                        <h2 className="text-lg font-bold text-slate-200 mb-2">Stack Operations</h2>
                        <p className="text-xs text-slate-400 mb-4">Observe how data is pushed and popped using Last-In-First-Out logic.</p>
                        
                        <div className="flex gap-3 mb-4">
                            <button
                                onClick={handlePush}
                                className="flex-1 py-2 text-xs font-bold rounded-xl bg-emerald-600 hover:bg-emerald-700 active:scale-95 transition"
                            >
                                📥 Push Random
                            </button>
                            <button
                                onClick={handlePop}
                                className="flex-1 py-2 text-xs font-bold rounded-xl bg-rose-600 hover:bg-rose-700 active:scale-95 transition"
                            >
                                📤 Pop Top
                            </button>
                        </div>

                        <div className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-3 h-48 overflow-y-auto">
                            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wide">Operation Logs</span>
                            <ul className="text-xs space-y-1.5 mt-2">
                                {stackLog.map((log, i) => (
                                    <li key={i} className="text-slate-300 border-b border-slate-800/50 pb-1 font-mono">
                                        &gt; {log}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>

                    <div className="flex flex-col items-center justify-end bg-slate-900/20 border border-slate-800/50 rounded-2xl p-6 h-80">
                        {/* Stack visual box */}
                        <div className="w-32 border-b-4 border-x-2 border-slate-700 rounded-b-xl flex flex-col-reverse gap-1.5 p-2 h-64 justify-start overflow-hidden">
                            {stack.map((val, idx) => (
                                <div
                                    key={idx}
                                    className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-mono font-bold text-center py-2.5 rounded-lg text-xs animate-bounce shadow-md shadow-indigo-500/10"
                                >
                                    {val}
                                    {idx === stack.length - 1 && <span className="block text-[8px] text-indigo-200">TOP</span>}
                                </div>
                            ))}
                            {stack.length === 0 && (
                                <div className="text-slate-600 text-[10px] text-center my-auto">Stack is empty</div>
                            )}
                        </div>
                    </div>
                </div>
            )}

            {/* Binary Search Panel */}
            {activeTab === "binary" && (
                <div className="bg-slate-950/80 border border-slate-800 p-5 rounded-2xl shadow-xl">
                    <h2 className="text-lg font-bold text-slate-200 mb-2">Binary Search Simulator</h2>
                    <p className="text-xs text-slate-400 mb-4">See how Binary Search narrows its left and right boundaries to locate the target in log(n) steps.</p>

                    {/* Controls */}
                    <div className="flex flex-wrap items-center gap-4 mb-6 bg-slate-900/60 p-4 border border-slate-800 rounded-xl">
                        <div className="flex-1 min-w-[200px]">
                            <label className="block text-[10px] font-bold text-slate-500 uppercase tracking-wide mb-1">Select Target Value</label>
                            <select
                                value={target}
                                onChange={(e) => {
                                    const val = parseInt(e.target.value);
                                    setTarget(val);
                                    resetBS(val);
                                }}
                                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs focus:border-indigo-500 outline-none"
                            >
                                {array.map((val) => (
                                    <option key={val} value={val}>{val}</option>
                                ))}
                                <option value={60}>60 (Not in Array)</option>
                            </select>
                        </div>
                        <div className="flex gap-2 w-full md:w-auto">
                            <button
                                onClick={stepBS}
                                disabled={bsState.finished}
                                className="flex-1 md:flex-none px-4 py-2 text-xs font-bold rounded-lg bg-indigo-600 hover:bg-indigo-700 disabled:opacity-30 disabled:cursor-not-allowed transition"
                            >
                                Next Step 🚀
                            </button>
                            <button
                                onClick={() => resetBS()}
                                className="flex-1 md:flex-none px-4 py-2 text-xs font-bold rounded-lg bg-slate-800 hover:bg-slate-700 transition"
                            >
                                Reset 🔄
                            </button>
                        </div>
                    </div>

                    {/* Array Cells */}
                    <div className="grid grid-cols-10 gap-2 mb-6">
                        {array.map((val, idx) => {
                            const isL = idx === bsState.left;
                            const isR = idx === bsState.right;
                            const isM = idx === bsState.mid;
                            const inRange = idx >= bsState.left && idx <= bsState.right;

                            let bgClass = "bg-slate-900/40 border-slate-800 text-slate-400";
                            if (isM) {
                                bgClass = bsState.found ? "bg-emerald-500 text-white border-emerald-400" : "bg-purple-600 text-white border-purple-500";
                            } else if (inRange) {
                                bgClass = "bg-slate-900 border-indigo-500/40 text-slate-200";
                            }

                            return (
                                <div key={idx} className="flex flex-col items-center">
                                    <div className="h-4 text-[8px] font-bold text-slate-500">
                                        {isL && "L"}
                                        {isR && " R"}
                                        {isM && " M"}
                                    </div>
                                    <div className={`w-full py-3 rounded-lg border text-center font-mono font-bold text-xs transition-all duration-300 ${bgClass}`}>
                                        {val}
                                    </div>
                                    <div className="text-[8px] text-slate-600 mt-1">idx {idx}</div>
                                </div>
                            );
                        })}
                    </div>

                    {/* status log banner */}
                    <div className="p-3.5 bg-slate-900/40 border border-slate-800/80 rounded-xl font-mono text-xs text-indigo-300">
                        &gt; {bsState.msg} (Step {bsState.step})
                    </div>
                </div>
            )}
        </div>
    );
}

// Bind visualizer render method
const rootNode = ReactDOM.createRoot(document.getElementById('react-root'));
rootNode.render(<AlgorithmVisualizer />);
