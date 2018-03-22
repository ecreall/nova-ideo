/* eslint-disable react/no-array-index-key, no-underscore-dangle */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import { I18n } from 'react-redux-i18n';
import Grow from 'material-ui/transitions/Grow';

import StatisticsDoughnut from '../common/Doughnut';
import { getEntityIcon } from '../../utils/processes';

const styles = {
  statisticsDoughnut: {
    marginTop: 0,
    marginBottom: 0,
    width: 30,
    height: 46
  },
  titleContainer: {
    display: 'flex',
    alignItems: 'center',
    transform: 'scale(0)'
  },
  title: {
    margin: 0,
    fontSize: 20,
    color: '#2c2d30',
    fontWeight: 900,
    lineHeight: 'normal'
  }
};

class IdeaAppBarTitle extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      titleVisible: true
    };
  }

  componentDidMount() {
    const { idea } = this.props;
    const scrollEvent = `${idea.id}-scroll`;
    document.addEventListener(scrollEvent, this.handleScroll);
  }

  componentWillUnmount() {
    const { idea } = this.props;
    const scrollEvent = `${idea.id}-scroll`;
    document.removeEventListener(scrollEvent, this.handleScroll);
  }

  handleScroll = (event) => {
    const { titleVisible } = this.state;
    const { scrollTop } = event.values;
    const titleIsVisible = scrollTop <= 100;
    if (titleVisible !== titleIsVisible) this.setState({ titleVisible: titleIsVisible });
  };

  render() {
    const { idea, hasEvaluation, stats, classes } = this.props;
    const { titleVisible } = this.state;
    const IdeaIcon = getEntityIcon(idea.__typename);
    return (
      <Grow in={!titleVisible} timeout={100}>
        <div className={classes.titleContainer}>
          <h1 className={classes.title}>
            <IdeaIcon className={classes.icon} />
            {idea && idea.title}
          </h1>
          {hasEvaluation &&
            <StatisticsDoughnut
              disableTotalCount
              classes={{
                statisticsDoughnut: classes.statisticsDoughnut
              }}
              title={I18n.t('evaluation.tokens')}
              elements={stats}
            />}
        </div>
      </Grow>
    );
  }
}

export default withStyles(styles)(IdeaAppBarTitle);