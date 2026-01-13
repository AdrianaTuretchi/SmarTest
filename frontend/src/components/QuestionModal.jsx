import React, { useState } from 'react';
import api from '../services/api';

const QuestionModal = ({ isOpen, onClose, questionType, questionData }) => {
  const [userAnswer, setUserAnswer] = useState('');
  const [feedbackResult, setFeedbackResult] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      const payload = {
        user_answer: userAnswer,
        raw_data: questionData.raw_data,
        template_id: questionData.template_id,
      };
      const response = await api.post(`/evaluate/${questionType}`, payload);
      setFeedbackResult(response.data);
    } catch (error) {
      console.error('Error submitting answer:', error);
      alert('Failed to submit answer. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white rounded shadow-xl p-6 w-full max-w-lg">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">{questionType} Question</h2>
          <button onClick={onClose} className="text-red-500 font-bold">X</button>
        </div>
        <div className="mb-4">
          <p className="text-lg font-medium">{questionData.question_text}</p>
        </div>
        <textarea
          className="w-full border rounded p-2 mb-4"
          rows="5"
          value={userAnswer}
          onChange={(e) => setUserAnswer(e.target.value)}
          placeholder="Enter your answer here... (e.g., JSON format for complex problems)"
        ></textarea>
        {feedbackResult ? (
          <div className="mt-4">
            <p className={`font-bold ${feedbackResult.score > 0 ? 'text-green-500' : 'text-red-500'}`}>
              Score: {feedbackResult.score}
            </p>
            <p>{feedbackResult.feedback_text}</p>
          </div>
        ) : (
          <button
            onClick={handleSubmit}
            className="bg-blue-500 text-white rounded px-4 py-2"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Submitting...' : 'Submit Answer'}
          </button>
        )}
      </div>
    </div>
  );
};

export default QuestionModal;