import React from 'react';
import { withStyles } from 'material-ui/styles';

import Tooltip from './overlay/Tooltip';
import OverlayTrigger from '../common/overlay/OverlayTrigger';

const styles = {
  tooltip: {
    '& .tooltip-inner': {
      backgroundColor: '#000000',
      padding: 10,
      maxWidth: 220
    }
  }
};

export const DumbOverlaidTooltip = ({ children, tooltip, placement, classes }) => {
  return (
    <OverlayTrigger
      overlay={
        <Tooltip className={classes.tooltip}>
          {tooltip}
        </Tooltip>
      }
      trigger={['hover']}
      placement={placement || 'top'}
    >
      {children}
    </OverlayTrigger>
  );
};

export default withStyles(styles)(DumbOverlaidTooltip);