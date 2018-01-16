import getExaminationComponent from './ExaminationAdapter';
import getTheme from './ThemeAdapter';

const getAllAdapters = (instanceId) => {
  return {
    examination: getExaminationComponent(instanceId),
    theme: getTheme(instanceId)
  };
};

export default getAllAdapters;