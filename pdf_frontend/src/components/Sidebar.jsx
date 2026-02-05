import { Link, useLocation } from "react-router-dom";
import { FileText, UploadCloud, LayoutDashboard, Settings } from "lucide-react";
import { cn } from "../utils/cn";
import { motion } from "framer-motion";

export default function Sidebar() {
    const location = useLocation();

    const navItems = [
        { name: "My Workspace", path: "/dashboard", icon: LayoutDashboard },
        { name: "Upload File", path: "/upload", icon: UploadCloud },
    ];

    return (
        <motion.aside
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="hidden md:flex flex-col w-64 h-screen fixed left-0 top-0 glass border-r border-border-glass z-50"
        >
            {/* Logo */}
            <div className="p-8 pb-4">
                <Link to="/" className="flex items-center space-x-3 group">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg shadow-primary/20 group-hover:scale-105 transition-transform duration-300">
                        <FileText className="w-6 h-6 text-white" />
                    </div>
                    <div>
                        <span className="block text-lg font-heading font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                            DocAnalyze
                        </span>
                        <span className="text-xs text-primary font-medium tracking-wider">LOCAL</span>
                    </div>
                </Link>
            </div>

            {/* Navigation */}
            <nav className="flex-1 px-4 py-8 space-y-2">
                <p className="px-4 text-xs font-semibold text-text-muted uppercase tracking-wider mb-4">Navigation</p>

                {navItems.map((item) => {
                    const isActive = location.pathname === item.path;
                    return (
                        <Link key={item.path} to={item.path}>
                            <div className={cn(
                                "relative flex items-center px-4 py-3 rounded-xl transition-all duration-200 group overflow-hidden",
                                isActive
                                    ? "bg-primary/10 text-white"
                                    : "text-text-muted hover:text-white hover:bg-white/5"
                            )}>
                                {isActive && (
                                    <motion.div
                                        layoutId="activeNav"
                                        className="absolute left-0 w-1 h-8 bg-primary rounded-r-full"
                                    />
                                )}
                                <item.icon className={cn(
                                    "w-5 h-5 mr-3 transition-colors",
                                    isActive ? "text-primary" : "group-hover:text-white"
                                )} />
                                <span className="font-medium">{item.name}</span>

                                {/* Hover Glow */}
                                {isActive && (
                                    <div className="absolute inset-0 bg-primary/5 blur-xl -z-10" />
                                )}
                            </div>
                        </Link>
                    );
                })}
            </nav>

            {/* Footer / Settings (Minimal) */}
            <div className="p-4 border-t border-border-glass">
                <button className="w-full flex items-center p-3 rounded-xl hover:bg-white/5 transition-colors text-text-muted hover:text-white">
                    <Settings className="w-5 h-5 mr-3" />
                    <span className="text-sm font-medium">Settings</span>
                </button>
            </div>
        </motion.aside>
    );
}
