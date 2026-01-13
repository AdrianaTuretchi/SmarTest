import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="bg-brand-bg min-h-screen flex flex-col items-center justify-center px-4">
      {/* Hero Section */}
      <div className="text-center max-w-3xl">
        {/* Logo / Title */}
        <h1 className="text-6xl md:text-7xl font-bold text-brand-primary mb-4">
          Smar<span className="text-brand-hover">Test</span>
        </h1>
        
        {/* Subtitle */}
        <p className="text-xl md:text-2xl text-brand-dark/80 mb-8">
          Platforma inteligentă pentru exersarea problemelor de Inteligență Artificială
        </p>
        
        {/* Description */}
        <p className="text-base text-brand-neutral mb-12 max-w-2xl mx-auto">
          Generează întrebări dinamice pentru Nash Equilibrium, CSP (Constraint Satisfaction Problems), 
          MinMax cu Alpha-Beta și alegerea strategiilor optime. Primește feedback instant și 
          justificări teoretice pentru fiecare răspuns.
        </p>
        
        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/practice"
            className="bg-brand-primary text-white px-8 py-4 rounded-lg text-lg font-semibold 
                       hover:bg-brand-hover transition-all shadow-lg hover:shadow-xl 
                       hover:shadow-brand-primary/30 transform hover:-translate-y-1"
          >
            Începe să exersezi
          </Link>
          
          <Link
            to="/tests"
            className="bg-brand-surface text-brand-dark px-8 py-4 rounded-lg text-lg font-semibold 
                       border-2 border-brand-primary hover:bg-brand-primary hover:text-white 
                       transition-all shadow-md hover:shadow-lg transform hover:-translate-y-1"
          >
            Mod Examen
          </Link>
        </div>
      </div>
      
      {/* Features Section */}
      <div className="mt-20 grid grid-cols-1 md:grid-cols-4 gap-6 max-w-5xl">
        <div className="bg-brand-surface p-6 rounded-lg shadow-md text-center border border-brand-neutral/20">
          <h3 className="font-semibold text-brand-dark mb-2">Nash Equilibrium</h3>
          <p className="text-sm text-brand-neutral">Matrici de plăți și echilibre pure</p>
        </div>
        
        <div className="bg-brand-surface p-6 rounded-lg shadow-md text-center border border-brand-neutral/20">
          <h3 className="font-semibold text-brand-dark mb-2">CSP</h3>
          <p className="text-sm text-brand-neutral">Backtracking, FC, MRV, AC-3</p>
        </div>
        
        <div className="bg-brand-surface p-6 rounded-lg shadow-md text-center border border-brand-neutral/20">
          <h3 className="font-semibold text-brand-dark mb-2">MinMax</h3>
          <p className="text-sm text-brand-neutral">Arbori de joc cu Alpha-Beta</p>
        </div>
        
        <div className="bg-brand-surface p-6 rounded-lg shadow-md text-center border border-brand-neutral/20">
          <h3 className="font-semibold text-brand-dark mb-2">Strategii</h3>
          <p className="text-sm text-brand-neutral">Alegerea algoritmului optim</p>
        </div>
      </div>
      
      {/* Footer hint */}
      <p className="mt-16 text-sm text-brand-neutral/60">
        Proiect realizat pentru disciplina Inteligență Artificială
      </p>
    </div>
  );
};

export default Home;