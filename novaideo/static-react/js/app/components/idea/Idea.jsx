/* eslint-disable react/no-array-index-key */
import React from 'react';
import { graphql } from 'react-apollo';
import { connect } from 'react-redux';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import Moment from 'moment';
import Grid from 'material-ui/Grid';
import { I18n } from 'react-redux-i18n';
import Avatar from 'material-ui/Avatar';
import Tooltip from 'material-ui/Tooltip';
import { CardActions } from 'material-ui/Card';
import IconButton from 'material-ui/IconButton';
import Icon from 'material-ui/Icon';
import { CircularProgress } from 'material-ui/Progress';
import { Scrollbars } from 'react-custom-scrollbars';

import ImagesPreview from '../common/ImagesPreview';
import Keywords from '../common/Keywords';
import IconWithText from '../common/IconWithText';
import Evaluation from '../common/Evaluation';
import StatisticsDoughnut, { createTooltip } from '../common/Doughnut';
import * as constants from '../../constants';
import { getActions } from '../../utils/entities';
import IdeaMenu from './IdeaMenu';
import IdeaActionsWrapper, { getEvaluationActions, getExaminationValue } from './IdeaActionsWrapper';
import { goTo, get } from '../../utils/routeMap';
import { ideaQuery } from '../../graphql/queries';
import Dialog from '../common/Dialog';
import { updateApp } from '../../actions/actions';
import Comments from '../channels/Comments';
import { styles as scrollbarStyles } from '../CollaborationApp';

const styles = (theme) => {
  return {
    ideaItem: {
      display: 'block',
      position: 'relative',
      height: '100%'
    },
    authorTitle: {
      display: 'flex',
      marginLeft: 4,
      alignItems: 'center'
    },
    header: {
      display: 'flex',
      flexDirection: 'column',
      margin: '0 10px',
      position: 'relative'
    },
    headerTitle: {
      fontSize: 15,
      color: '#2c2d30',
      fontWeight: 900,
      lineHeight: 'normal'
    },
    titleContainer: {
      display: 'flex'
    },
    title: {
      fontSize: 42,
      color: '#2c2d30',
      fontWeight: 900,
      paddingTop: 3,
      lineHeight: 'normal'
    },
    headerAddOn: {
      color: '#999999ff',
      fontSize: 12,
      lineHeight: 'normal'
    },
    body: {
      display: 'flex',
      flexDirection: 'column',
      width: '100%'
    },
    bodyTitle: {
      marginLeft: -3,
      marginBottom: 10,
      cursor: 'pointer'
    },
    left: {
      display: 'flex',
      alignItems: 'center',
      paddingRight: 10,
      margin: '8px 0',
      flexDirection: 'column'
    },
    right: {
      float: 'right'
    },
    leftActions: {
      display: 'flex',
      flex: 1,
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      paddingTop: 15
    },
    bodyContent: {
      display: 'flex',
      justifyContent: 'space-between',
      flexDirection: 'column',
      width: '100%',
      height: '100%'
    },
    textContainer: {
      display: 'flex',
      justifyContent: 'space-between'
    },
    bodyFooter: {
      display: 'flex',
      flexDirection: 'row',
      marginTop: 10
    },
    actionsContainer: {
      height: 41
    },
    actionsText: {
      fontSize: 16,
      color: '#717171',
      fontWeight: '700',
      marginRight: 15,
      '&:hover': {
        color: theme.palette.primary['500']
      }
    },
    actionsIcon: {
      fontWeight: 100,
      fontSize: '19px !important',
      marginRight: 5,
      marginTop: -4
    },
    avatar: {
      borderRadius: 4
    },
    anonymousAvatar: {
      color: theme.palette.tertiary.hover.color,
      backgroundColor: theme.palette.tertiary.color,
      fontWeight: 900
    },
    tooltipSupport: {
      position: 'absolute',
      '& .tooltip-inner': {
        backgroundColor: '#4eaf4e'
      }
    },
    tooltipOppose: {
      position: 'absolute',
      '& .tooltip-inner': {
        backgroundColor: '#ef6e18'
      }
    },
    ideaText: {
      fontSize: 18,
      fontWeight: 400,
      fontStyle: 'normal',
      lineHeight: 1.58,
      letterSpacing: '-.003em',
      '& a': {
        color: '#0576b9',
        textDecoration: 'none',
        '&:hover': {
          textDecoration: 'underline'
        }
      },
      '& p': {
        margin: 0
      }
    },
    imagesContainer: {
      minWidth: 300,
      float: 'right',
      padding: '0 0 0 8px !important'
    },
    root: {
      height: 'calc(100vh - 66px)',
      overflow: 'auto'
    },
    maxContainer: {
      paddingLeft: 20,
      paddingRight: 20,
      maxWidth: 740,
      marginRight: 'auto',
      marginLeft: 'auto',
      marginTop: 30
    },
    statisticsDoughnut: {
      marginTop: 0,
      marginBottom: 0
    },
    appBarContainer: {
      display: 'flex',
      justifyContent: 'space-between'
    },
    commentComntainer: {
      width: '100%',
      maxHeight: 600,
      margin: '20px 0',
      borderRadius: 6,
      boxShadow: '0 1px 2px rgba(128, 128, 128, 0.25)'
    },
    comments: {
      padding: '0 !important',
      borderRadius: 6
    },
    commentFormContainer: {
      padding: 0
    }
  };
};

export class DumbIdea extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      open: this.props.open
    };
  }

  close = () => {
    this.setState({ open: false }, () => {
      goTo(this.props.previousLocation || get('root'));
    });
  };

  render() {
    const { classes, data, site, adapters } = this.props;
    if (data.loading) {
      return (
        <div className={classes.progress}>
          <CircularProgress size={30} />
        </div>
      );
    }
    const { idea } = data;
    const { open } = this.state;
    const author = idea.author;
    const authorPicture = author.picture;
    const isAnonymous = author.isAnonymous;
    const today = Moment();
    const isToday = today.isSame(Moment(idea.createdAt), 'day');
    const yesterday = today.subtract(1, 'days').startOf('day');
    const isYesterday = yesterday.isSame(Moment(idea.createdAt), 'day');
    const format = (isToday && 'date.todayFormat') || (isYesterday && 'date.yesterdayFormat') || 'date.format3';
    const createdAtF3 = Moment(idea.createdAt).format(I18n.t(format));
    const images = idea.attachedFiles
      ? idea.attachedFiles.filter((image) => {
        return image.isImage;
      })
      : [];
    const hasEvaluation = site.supportIdeas && idea.state.includes('published');
    const Examination = adapters.examination;
    const communicationActions = getActions(idea.actions, constants.ACTIONS.communicationAction);
    return (
      <Dialog
        classes={{
          container: classes.ideaItem
        }}
        appBar={
          <div className={classes.appBarContainer}>
            <div className={classes.titleContainer}>
              <Avatar
                className={isAnonymous && classes.anonymousAvatar}
                classes={{ root: classes.avatar }}
                src={authorPicture ? `${authorPicture.url}/profil` : ''}
              >
                {isAnonymous && <Icon className={'mdi-set mdi-guy-fawkes-mask'} />}
              </Avatar>
              <div className={classes.header}>
                <span className={classes.headerTitle}>
                  {author.title}
                </span>
                <span className={classes.headerAddOn}>
                  {createdAtF3}
                </span>
              </div>

              <IdeaMenu
                initRef={(menu) => {
                  this.menu = menu;
                }}
                idea={idea}
              />
            </div>
            <CardActions classes={{ root: classes.actionsContainer }} disableActionSpacing>
              {communicationActions.map((action, key) => {
                return (
                  <IconButton
                    className={classes.actionsText}
                    key={key}
                    onClick={() => {
                      return this.props.actionsManager.performAction(action);
                    }}
                    aria-label="todo"
                  >
                    <Icon className={classNames(action.stylePicto, classes.actionsIcon)} />
                    {action.counter}
                  </IconButton>
                );
              })}
            </CardActions>
          </div>
        }
        fullScreen
        open={open}
        onClose={this.close}
      >
        <div className={classes.root}>
          <Scrollbars
            renderTrackVertical={(props) => {
              return <div {...props} style={{ ...props.style, ...scrollbarStyles.trackVertical }} />;
            }}
            renderThumbVertical={(props) => {
              return <div {...props} style={{ ...props.style, ...scrollbarStyles.thumbVertical }} />;
            }}
          >
            <div className={classes.maxContainer}>
              {hasEvaluation &&
                <div className={classes.right}>
                  <StatisticsDoughnut
                    classes={{
                      statisticsDoughnut: classes.statisticsDoughnut
                    }}
                    title={I18n.t('evaluation.tokens')}
                    elements={[
                      {
                        color: '#4eaf4e',
                        count: idea.tokensSupport,
                        Tooltip: createTooltip(I18n.t('evaluation.support'), idea.tokensSupport, classes.tooltipSupport)
                      },
                      {
                        color: '#ef6e18',
                        count: idea.tokensOpposition,
                        Tooltip: createTooltip(I18n.t('evaluation.opposition'), idea.tokensOpposition, classes.tooltipOppose)
                      }
                    ]}
                  />
                </div>}
              <h1 className={classes.title}>
                <Icon className={classNames('mdi-set mdi-lightbulb', classes.icon)} />
                {idea && idea.title}
              </h1>
              {images.length > 0 &&
                <div className={classes.imagesContainer}>
                  <ImagesPreview images={images} />
                </div>}
              <div className={classes.ideaText} dangerouslySetInnerHTML={{ __html: idea.text }} />

              <Comments
                classes={{
                  container: classes.commentComntainer,
                  comments: classes.comments,
                  formContainer: classes.commentFormContainer
                }}
                rightDisabled
                formTop
                channel={idea.channel.id}
              />
            </div>
          </Scrollbars>
        </div>
      </Dialog>
    );
  }
}

function DumbIdeaItem(props) {
  return (
    <IdeaActionsWrapper idea={props.data.idea}>
      <DumbIdea {...props} />
    </IdeaActionsWrapper>
  );
}

export const mapDispatchToProps = {
  updateApp: updateApp
};

export const mapStateToProps = (state) => {
  return {
    previousLocation: state.history.navigation.previous,
    site: state.globalProps.site,
    adapters: state.adapters
  };
};

export default withStyles(styles, { withTheme: true })(
  connect(mapStateToProps, mapDispatchToProps)(
    graphql(ideaQuery, {
      options: (props) => {
        return {
          fetchPolicy: 'cache-first',
          variables: { id: props.id }
        };
      }
    })(DumbIdeaItem)
  )
);