import defaultTheme from '../../theme';
import timeoTheme from './timeo/theme';

const getTheme = (instanceId) => {
  switch (instanceId) {
  case 'timeo':
    return timeoTheme;
  default:
    return defaultTheme;
  }
};

export default getTheme;