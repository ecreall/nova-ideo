import { OPINIONS } from '../../constants';
import { OPINIONS as TIMO_OPINIONS } from './timeo/constants';

const getOpinions = (instanceId) => {
  switch (instanceId) {
  case 'timeo':
    return TIMO_OPINIONS;
  default:
    return OPINIONS;
  }
};

export default getOpinions;