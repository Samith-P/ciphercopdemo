import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export const useFeatureAuth = () => {
  const { isAuthenticated, isLoading } = useAuth();
  const navigate = useNavigate();

  const checkAuthForFeature = (callback) => {
    if (isLoading) return;
    
    if (!isAuthenticated) {
      // Store the current path to redirect back after login
      const currentPath = window.location.pathname;
      navigate('/login', { state: { from: { pathname: currentPath } } });
      return false;
    }
    
    // User is authenticated, proceed with the feature
    if (callback) callback();
    return true;
  };

  return {
    isAuthenticated,
    isLoading,
    checkAuthForFeature
  };
};
