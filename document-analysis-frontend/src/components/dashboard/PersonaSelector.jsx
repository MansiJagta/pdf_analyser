import React from 'react';
import { motion } from 'framer-motion';
import { User, Brain, Scale } from 'lucide-react';
import Card from '../ui/Card';

export default function PersonaSelector({ selectedPersona, setSelectedPersona }) {
  const personas = [
    { 
      id: 'executive', 
      icon: User, 
      label: 'Executive', 
      color: 'cyan', 
      desc: 'High-level insights',
      features: 'Strategic summaries, KPIs, action items'
    },
    { 
      id: 'researcher', 
      icon: Brain, 
      label: 'Researcher', 
      color: 'purple', 
      desc: 'Deep analysis',
      features: 'Detailed findings, methodology, citations'
    },
    { 
      id: 'legal', 
      icon: Scale, 
      label: 'Legal', 
      color: 'green', 
      desc: 'Compliance focus',
      features: 'Risk assessment, obligations, clauses'
    }
  ];
  
  return (
    <Card>
      <h3 className="text-lg font-semibold text-white mb-4">Analysis Persona</h3>
      <p className="text-sm text-gray-400 mb-4">
        Choose how the AI should analyze your document
      </p>
      
      <div className="grid grid-cols-3 gap-3">
        {personas.map(persona => {
          const isSelected = selectedPersona === persona.id;
          return (
            <motion.button
              key={persona.id}
              whileHover={{ scale: 1.05, y: -2 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setSelectedPersona(persona.id)}
              className={`p-4 rounded-lg border transition-all ${
                isSelected
                  ? 'bg-cyan-500/20 border-cyan-500/50 text-cyan-300 glow-cyan-soft'
                  : 'bg-white/5 border-white/10 text-gray-400 hover:border-white/20'
              }`}
            >
              <persona.icon className={`w-6 h-6 mx-auto mb-2 ${
                isSelected ? 'text-cyan-400' : 'text-gray-500'
              }`} />
              <p className="text-sm font-medium mb-1">{persona.label}</p>
              <p className="text-xs opacity-70">{persona.desc}</p>
            </motion.button>
          );
        })}
      </div>
      
      {/* Selected Persona Details */}
      <div className="mt-4 p-4 bg-white/5 rounded-lg border border-white/10">
        <p className="text-xs text-gray-400 mb-1">Active Mode:</p>
        <p className="text-sm text-white font-medium">
          {personas.find(p => p.id === selectedPersona)?.features}
        </p>
      </div>
    </Card>
  );
}