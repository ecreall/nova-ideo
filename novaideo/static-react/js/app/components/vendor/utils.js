import getTheme from './ThemeAdapter';

const getAllAdapters = (instanceId) => {
  return {
    theme: getTheme(instanceId)
  };
};

export default getAllAdapters;