import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Sparkles, RefreshCw } from "lucide-react";
import { cn } from "../utils/cn";
import { motion, AnimatePresence } from "framer-motion";

export default function ChatInterface({ docName }) {
    const [messages, setMessages] = useState([
        { id: 1, role: "ai", content: `Hello! I'm ready to answer questions about **${docName}**.` }
    ]);
    const [input, setInput] = useState("");
    const [isTyping, setIsTyping] = useState(false);
    const scrollRef = useRef(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages, isTyping]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMsg = { id: Date.now(), role: "user", content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput("");
        setIsTyping(true);

        setTimeout(() => {
            const aiMsg = {
                id: Date.now() + 1,
                role: "ai",
                content: "Here is the insight you requested. In a real scenario, this would be retrieved from the vector database based on your query context."
            };
            setMessages(prev => [...prev, aiMsg]);
            setIsTyping(false);
        }, 1200);
    };

    return (
        <div className="flex flex-col h-full bg-[#181b21] rounded-2xl border border-white/5 overflow-hidden shadow-2xl relative">

            {/* Chat Header */}
            <div className="p-4 border-b border-white/5 bg-[#181b21] flex items-center justify-between z-10">
                <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 rounded-lg bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center">
                        <Bot className="w-4 h-4 text-indigo-400" />
                    </div>
                    <div>
                        <h3 className="font-bold text-white text-sm">Assistant</h3>
                        <p className="text-[10px] text-emerald-400 font-medium">Online</p>
                    </div>
                </div>
                <button onClick={() => setMessages([])} className="text-slate-500 hover:text-white transition-colors">
                    <RefreshCw className="w-4 h-4" />
                </button>
            </div>

            {/* Messages */}
            <div
                ref={scrollRef}
                className="flex-1 overflow-y-auto p-6 space-y-6 scroll-smooth bg-[url('/noise.png')] bg-opacity-5"
            >
                <AnimatePresence initial={false}>
                    {messages.map((msg) => (
                        <motion.div
                            key={msg.id}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={cn("flex w-full", msg.role === "ai" ? "justify-start" : "justify-end")}
                        >
                            <div className={cn("max-w-[85%]", msg.role === "ai" ? "flex gap-3" : "")}>
                                {msg.role === "ai" && (
                                    <div className="w-8 h-8 rounded-full bg-[#22262e] border border-white/5 flex items-center justify-center flex-shrink-0 mt-1">
                                        <Sparkles className="w-4 h-4 text-cyan-400" />
                                    </div>
                                )}

                                <div className={cn(
                                    "p-4 rounded-2xl text-sm leading-relaxed shadow-sm",
                                    msg.role === "ai"
                                        ? "bg-[#22262e] border border-white/5 text-slate-200"
                                        : "bg-gradient-to-br from-cyan-600 to-indigo-600 text-white"
                                )}>
                                    <p>{msg.content}</p>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>

                {isTyping && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} class="flex gap-3">
                        <div className="w-8 h-8 rounded-full bg-[#22262e] border border-white/5 flex items-center justify-center flex-shrink-0">
                            <Bot className="w-4 h-4 text-slate-500" />
                        </div>
                        <div className="bg-[#22262e] border border-white/5 p-3 rounded-2xl rounded-tl-none flex items-center gap-1">
                            <span className="w-1.5 h-1.5 bg-slate-500 rounded-full animate-bounce" />
                            <span className="w-1.5 h-1.5 bg-slate-500 rounded-full animate-bounce delay-100" />
                            <span className="w-1.5 h-1.5 bg-slate-500 rounded-full animate-bounce delay-200" />
                        </div>
                    </motion.div>
                )}
            </div>

            {/* Input Area */}
            <div className="p-5 bg-[#181b21] border-t border-white/5">
                <form onSubmit={handleSend} className="relative group">
                    <div className="relative flex items-center bg-[#0f1115] border border-white/10 rounded-xl overflow-hidden shadow-inner focus-within:ring-1 focus-within:ring-cyan-500/50 transition-all">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Ask something..."
                            className="flex-1 bg-transparent text-white pl-4 pr-12 py-4 focus:outline-none placeholder:text-slate-600"
                        />
                        <div className="pr-2">
                            <button
                                type="submit"
                                disabled={!input.trim()}
                                className="p-2 bg-white/5 hover:bg-white text-slate-400 hover:text-black rounded-lg transition-all disabled:opacity-30 disabled:hover:bg-transparent disabled:hover:text-slate-400"
                            >
                                <Send className="w-4 h-4" />
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    );
}
