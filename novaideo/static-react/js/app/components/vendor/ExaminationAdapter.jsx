import DefaultExamination from '../common/Examination';
import TimeoExamination from './timeo/Examination';

const getExaminationComponent = (instanceId) => {
  switch (instanceId) {
  case 'timeo':
    return TimeoExamination;
  default:
    return DefaultExamination;
  }
};

export default getExaminationComponent;