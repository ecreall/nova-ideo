import { teal, blue } from '@material-ui/core/colors';

import { getTheme } from '../../../theme';

const timioTheme = {
  primaryColor: teal[500],
  secondaryColor: blue[500]
};

export default getTheme(timioTheme);