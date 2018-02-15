/* eslint-disable react/no-array-index-key */
import React from 'react';
import { graphql } from 'react-apollo';
import { connect } from 'react-redux';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import { I18n } from 'react-redux-i18n';
import Icon from 'material-ui/Icon';
import { CircularProgress } from 'material-ui/Progress';
import { Scrollbars } from 'react-custom-scrollbars';

import ImagesPreview from '../common/ImagesPreview';
import StatisticsDoughnut, { createTooltip } from '../common/Doughnut';
import AllignedActions from '../common/AllignedActions';
import Dialog from '../common/Dialog';
import * as constants from '../../constants';
import { getActions } from '../../utils/entities';
import { goTo, get } from '../../utils/routeMap';
import { getFormattedDate } from '../../utils/globalFunctions';
import { ideaQuery } from '../../graphql/queries';
import UserAvatar from '../user/UserAvatar';
import Comments from '../channels/Comments';
import { styles as scrollbarStyles } from '../CollaborationApp';
import IdeaMenu from './IdeaMenu';
import IdeaActionsWrapper, { getEvaluationActions, getExaminationValue } from './IdeaActionsWrapper';

const styles = (theme) => {
  return {
    container: {
      display: 'block',
      position: 'relative',
      height: '100%'
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
    actionsContainer: {
      height: 41,
      width: 'auto'
    },
    actionsText: {
      color: '#2c2d30',
      marginRight: 15,
      fontSize: 14,
      fontWeight: 400,
      width: 35,
      '&:hover': {
        color: theme.palette.info['700']
      }
    },
    actionsIcon: {
      fontWeight: 100,
      fontSize: '20px !important',
      marginRight: 5,
      marginTop: -2
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
    right: {
      float: 'right'
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
      height: '100%',
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
    },
    commentsList: {
      height: '100%',
      paddingBottom: 20,
      paddingTop: 20
    },
    closeBtn: {
      '&::after': {
        display: 'block',
        position: 'absolute',
        top: '50%',
        right: 'auto',
        bottom: 'auto',
        left: -4,
        height: 20,
        transform: 'translateY(-50%)',
        borderRadius: 0,
        borderRight: '1px solid #e5e5e5',
        content: '""',
        color: '#2c2d30'
      }
    }
  };
};

export class RunderIdea extends React.Component {
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
    const createdAtF3 = getFormattedDate(idea.createdAt, 'date.format3');
    const images = idea.attachedFiles
      ? idea.attachedFiles.filter((image) => {
        return image.isImage;
      })
      : [];
    const hasEvaluation = site.supportIdeas && idea.state.includes('published');
    const communicationActions = getActions(idea.actions, { descriminator: constants.ACTIONS.communication });
    const scrollEvent = `${idea.id}-scroll`;
    return (
      <Dialog
        classes={{
          container: classes.container,
          closeBtn: classes.closeBtn
        }}
        appBar={
          <div className={classes.appBarContainer}>
            <div className={classes.titleContainer}>
              <UserAvatar isAnonymous={isAnonymous} picture={authorPicture} title={author.title} />
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
            <AllignedActions
              actions={communicationActions}
              onActionClick={this.props.actionsManager.performAction}
              classes={{
                actionsContainer: classes.actionsContainer,
                actionsText: classes.actionsText,
                actionsIcon: classes.actionsIcon
              }}
            />
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
            onScrollFrame={(values) => {
              const event = document.createEvent('HTMLEvents');
              event.initEvent(scrollEvent, true, true);
              event.values = values;
              document.dispatchEvent(event);
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
                channelId={idea.channel.id}
                fetchMoreOnEvent={scrollEvent}
                classes={{
                  container: classes.commentComntainer,
                  comments: classes.comments,
                  formContainer: classes.commentFormContainer,
                  list: classes.commentsList
                }}
                rightDisabled
                fullScreen
                ignorDrawer
                formTop
              />
            </div>
          </Scrollbars>
        </div>
      </Dialog>
    );
  }
}

function DumbIdea(props) {
  const { data, onActionClick } = props;
  return (
    <IdeaActionsWrapper idea={data.idea} onActionClick={onActionClick}>
      <RunderIdea {...props} />
    </IdeaActionsWrapper>
  );
}

export const mapStateToProps = (state) => {
  return {
    previousLocation: state.history.navigation.previous,
    site: state.globalProps.site,
    adapters: state.adapters
  };
};

export default withStyles(styles, { withTheme: true })(
  connect(mapStateToProps)(
    graphql(ideaQuery, {
      options: (props) => {
        return {
          fetchPolicy: 'cache-first',
          variables: { id: props.id }
        };
      }
    })(DumbIdea)
  )
);