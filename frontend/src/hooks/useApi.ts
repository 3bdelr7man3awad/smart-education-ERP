import { useState, useCallback } from 'react';
import { health } from '../services/api';

export const useApi = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const testConnection = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await health.check();
      return response.data;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    isLoading,
    error,
    testConnection,
  };
}; 