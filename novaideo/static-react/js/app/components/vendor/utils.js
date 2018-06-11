import getExaminationComponent from './ExaminationAdapter';
import getTheme from './ThemeAdapter';
import getOpinions from './OpinionsAdapter';

const getAllAdapters = (instanceId) => {
  return {
    examination: getExaminationComponent(instanceId),
    theme: getTheme(instanceId),
    opinions: getOpinions(instanceId)
  };
};

export default getAllAdapters;