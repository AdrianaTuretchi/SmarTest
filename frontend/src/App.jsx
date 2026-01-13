import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import PracticePage from './pages/PracticePage';
import TestConfigPage from './pages/TestConfigPage';
import TestActivePage from './pages/TestActivePage';
import TestResultsPage from './pages/TestResultsPage';
import SolverPage from './pages/SolverPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/practice" element={<PracticePage />} />
        <Route path="/tests" element={<TestConfigPage />} />
        <Route path="/tests/active" element={<TestActivePage />} />
        <Route path="/tests/results" element={<TestResultsPage />} />
        <Route path="/solver" element={<SolverPage />} />
      </Routes>
    </Router>
  );
}

export default App;
