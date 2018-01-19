import React from 'react';
import { withStyles } from 'material-ui/styles';

import Tooltip from './overlay/Tooltip';
import Doughnut from '../svg/doughnut';

const styles = {
  statisticsDoughnut: {
    textAlign: 'center',
    display: 'inline-block',
    height: 100,
    marginTop: 30,
    marginBottom: 30,
    minWidth: 150,
    padding: '0 0 0',
    right: 0,
    width: '20%',
    '& .circle': {
      strokeWidth: 16,
      fill: 'transparent'
    }
  },
  statistics: {
    position: 'relative',
    width: '100%',
    height: '100%',
    display: 'flex',
    flexDirection: 'column'
  },
  superpose: {
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    '& svg': {
      width: '100%',
      height: '100%'
    }
  },
  labelSuperpose: {
    position: 'absolute',
    top: '48%',
    left: '50%',
    transform: 'translateX(-50%) translateY(-50%)',
    width: 'auto',
    height: 'auto'
  },
  after: {},
  doughnutLabelCount: {
    fontSize: 16,
    letterSpacing: 'initial',
    fontWeight: 900
  },
  doughnutLabelText: {
    fontFamily: 'LatoWebLight',
    fontSize: 10,
    letterSpacing: 'initial'
  }
};

export const createTooltip = (title, count, className) => {
  return (
    <Tooltip className={className}>
      {count} {title}
    </Tooltip>
  );
};

const StatisticsDoughnut = ({ elements, placement, title, classes }) => {
  const totalCount = elements.reduce((result, element) => {
    return result + element.count;
  }, 0);
  const placeAfter = placement === 'after';
  return (
    <div className={classes.statisticsDoughnut}>
      <div className={classes.statistics}>
        <div className={!placeAfter && classes.superpose}>
          <Doughnut elements={elements} />
        </div>
        <div className={placeAfter ? classes.after : classes.labelSuperpose}>
          <div className={classes.doughnutLabelCount}>
            {totalCount}
          </div>
          {placeAfter ? ' ' : ''}
          <div className={classes.doughnutLabelText}>
            {title}
          </div>
        </div>
      </div>
    </div>
  );
};

export default withStyles(styles)(StatisticsDoughnut);