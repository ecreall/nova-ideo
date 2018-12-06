/* eslint-disable react/no-array-index-key, no-undef */
import React from 'react';
import { graphql } from 'react-apollo';
import { withStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';
import { Translate } from 'react-redux-i18n';

import ObjectStats from '../../graphql/queries/ObjectStats.graphql';
import StatisticsDoughnut, { createTooltip } from './Doughnut';

const styles = {
  progress: {
    width: '100%',
    display: 'flex',
    justifyContent: 'center'
  },
  stats: {
    display: 'flex'
  },
  tooltipSupport: {
    position: 'absolute',
    '& .tooltip-inner': {
      backgroundColor: '#4eaf4e'
    },
    '& .tooltip-arrow': {
      borderBottomColor: '#4eaf4e !important',
      borderTopColor: '#4eaf4e !important'
    }
  },
  tooltipOppose: {
    position: 'absolute',
    '& .tooltip-inner': {
      backgroundColor: '#ef6e18'
    },
    '& .tooltip-arrow': {
      borderBottomColor: '#ef6e18 !important',
      borderTopColor: '#ef6e18 !important'
    }
  },
  tooltipFavorable: {
    position: 'absolute',
    '& .tooltip-inner': {
      backgroundColor: '#4eaf4e'
    },
    '& .tooltip-arrow': {
      borderBottomColor: '#4eaf4e !important',
      borderTopColor: '#4eaf4e !important'
    }
  },
  tooltipUnfavorable: {
    position: 'absolute',
    '& .tooltip-inner': {
      backgroundColor: '#f13b2d'
    },
    '& .tooltip-arrow': {
      borderBottomColor: '#f13b2d !important',
      borderTopColor: '#f13b2d !important'
    }
  },
  tooltipToStudy: {
    position: 'absolute',
    '& .tooltip-inner': {
      backgroundColor: '#ef6e18'
    },
    '& .tooltip-arrow': {
      borderBottomColor: '#ef6e18 !important',
      borderTopColor: '#ef6e18 !important'
    }
  },
  statisticsDoughnut: {
    margin: 0,
    width: 60,
    height: 60,
    minWidth: 60,
    '& .circle': {
      strokeWidth: 10
    }
  },
  doughnutLabelCount: {
    fontSize: 13,
    color: '#1f1f21'
  }
};

export function getObjectSupportStats(stats, classes) {
  return [
    {
      color: '#4eaf4e',
      count: stats.evaluationStats.support,
      Tooltip: createTooltip(
        <Translate value="evaluation.support" count={stats.evaluationStats.support} />,
        stats.evaluationStats.support,
        classes.tooltipSupport
      )
    },
    {
      color: '#ef6e18',
      count: stats.evaluationStats.opposition,
      Tooltip: createTooltip(
        <Translate value="evaluation.opposition" count={stats.evaluationStats.opposition} />,
        stats.evaluationStats.opposition,
        classes.tooltipOppose
      )
    }
  ];
}

export function getObjectExaminationStats(stats, classes) {
  return [
    {
      color: '#4eaf4e',
      count: stats.examinationStats.favorable,
      Tooltip: createTooltip(
        <Translate value="examination.favorable" count={stats.examinationStats.favorable} />,
        stats.examinationStats.favorable,
        classes.tooltipFavorable
      )
    },
    {
      color: '#f13b2d',
      count: stats.examinationStats.unfavorable,
      Tooltip: createTooltip(
        <Translate value="examination.unfavorable" count={stats.examinationStats.unfavorable} />,
        stats.examinationStats.unfavorable,
        classes.tooltipUnfavorable
      )
    },
    {
      color: '#ef6e18',
      count: stats.examinationStats.toStudy,
      Tooltip: createTooltip(
        <Translate value="examination.toStudy" count={stats.examinationStats.toStudy} />,
        stats.examinationStats.toStudy,
        classes.tooltipToStudy
      )
    }
  ];
}

export const DumbObjectStats = ({ data, classes }) => {
  const { stats } = data;
  if (!stats) {
    return (
      <div className={classes.progress}>
        <CircularProgress disableShrink size={30} />
      </div>
    );
  }
  return (
    <div className={classes.stats}>
      <StatisticsDoughnut
        caption="evaluation.tokens"
        elements={getObjectSupportStats(stats, classes)}
        classes={{
          statisticsDoughnut: classes.statisticsDoughnut,
          doughnutLabelCount: classes.doughnutLabelCount
        }}
      />
      <StatisticsDoughnut
        caption="examination.examin"
        elements={getObjectExaminationStats(stats, classes)}
        classes={{
          statisticsDoughnut: classes.statisticsDoughnut,
          doughnutLabelCount: classes.doughnutLabelCount
        }}
      />
    </div>
  );
};

export default withStyles(styles)(
  graphql(ObjectStats, {
    options: (props) => {
      return {
        fetchPolicy: 'cache-and-network',
        variables: { id: props.id }
      };
    }
  })(DumbObjectStats)
);