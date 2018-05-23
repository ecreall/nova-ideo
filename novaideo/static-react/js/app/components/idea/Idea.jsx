/* eslint-disable react/no-array-index-key, no-underscore-dangle */
import React from 'react';
import { graphql } from 'react-apollo';
import { connect } from 'react-redux';
import { withStyles } from '@material-ui/core/styles';
import classNames from 'classnames';
import Icon from '@material-ui/core/Icon';
import Button from '@material-ui/core/Button';
import Zoom from '@material-ui/core/Zoom';

import ImagesPreview from '../common/ImagesPreview';
import FilesPreview from '../common/FilesPreview';
import Anchor from '../common/Anchor';
import StatisticsDoughnut from '../common/Doughnut';
import Dialog from '../common/Dialog';
import { ACTIONS, STATE } from '../../processes';
import { goTo, get } from '../../utils/routeMap';
import { getEntityIcon } from '../../utils/processes';
import Idea from '../../graphql/queries/Idea.graphql';
import Comments from '../chatApp/Comments';
import Scrollbar from '../common/Scrollbar';
import Evaluation from '../common/Evaluation';
import IdeaProcessManager from './IdeaProcessManager';
import IdeaAppBar from './IdeaAppBar';
import { getEvaluationIcons, getEvaluationActions, getExaminationValue, getIdeaSupportStats, getExaminationTtile } from '.';
import { MediumEditor } from '../forms/widgets/mediumEditor';

const styles = (theme) => {
  return {
    container: {
      display: 'block',
      position: 'relative',
      height: '100%'
    },
    title: {
      fontSize: 30,
      color: '#2c2d30',
      fontWeight: 900,
      paddingTop: 3,
      lineHeight: 'normal'
    },
    tooltipSupport: {
      position: 'absolute',
      '& .tooltip-inner': {
        backgroundColor: '#4eaf4e'
      },
      '& .tooltip-arrow': {
        borderBottomColor: '#4eaf4e !important'
      }
    },
    tooltipOppose: {
      position: 'absolute',
      '& .tooltip-inner': {
        backgroundColor: '#ef6e18'
      },
      '& .tooltip-arrow': {
        borderBottomColor: '#ef6e18 !important'
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
      padding: '0 0 0 8px !important',
      zIndex: 1000,
      position: 'relative'
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
    },
    leftActions: {
      position: 'fixed',
      marginLeft: -120,
      top: '0 !important',
      transform: 'translateY(170px)',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center'
    },
    goToComments: {
      width: 50,
      height: 50,
      fontSize: 24,
      backgroundColor: 'white',
      color: theme.palette.primary[500],
      marginTop: 13,
      boxShadow: 'none',
      border: 'solid 1px rgba(128, 128, 128, 0.5)',
      '&:hover': {
        backgroundColor: 'white'
      }
    },
    goToCommentsIcon: {
      marginTop: 3,
      marginLeft: 2
    },
    goToTop: {
      position: 'fixed',
      bottom: 20,
      right: 20
    },
    goToTopBtn: {
      width: 50,
      height: 50,
      fontSize: 24,
      backgroundColor: theme.palette.tertiary.color,
      color: theme.palette.tertiary.hover.color,
      marginTop: 13,
      '&:hover': {
        backgroundColor: theme.palette.tertiary.color
      }
    },
    goToTopIcon: {
      marginTop: 3,
      marginLeft: 2
    }
  };
};

export class DumbIdea extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      open: true
    };
  }

  comments = null;

  title = null;

  close = () => {
    this.setState({ open: false }, () => {
      goTo(get('root'));
    });
  };

  render() {
    const { classes, data, site, processManager, adapters } = this.props;
    const { idea } = data;
    if (data.loading || !idea) {
      return null;
    }
    const { open } = this.state;
    const images = idea.attachedFiles
      ? idea.attachedFiles.filter((file) => {
        return file.isImage;
      })
      : [];
    const files = idea.attachedFiles
      ? idea.attachedFiles.filter((file) => {
        return !file.isImage;
      })
      : [];
    const hasEvaluation = site.supportIdeas && idea.state.includes(STATE.idea.published);
    const scrollEvent = `${idea.id}-scroll`;
    const Examination = adapters.examination;
    const stats = getIdeaSupportStats(idea, classes);
    const IdeaIcon = getEntityIcon(idea.__typename);
    return (
      <Dialog
        withDrawer
        classes={{
          container: classes.container,
          closeBtn: classes.closeBtn
        }}
        appBar={<IdeaAppBar idea={idea} processManager={processManager} hasEvaluation={hasEvaluation} stats={stats} />}
        fullScreen
        open={open}
        onClose={this.close}
        transition={Zoom}
      >
        <div className={classes.root}>
          <Scrollbar scrollEvent={scrollEvent}>
            <div className={classes.maxContainer}>
              <div className={classes.leftActions}>
                {hasEvaluation
                  ? <Evaluation
                    big
                    icon={getEvaluationIcons(idea.userToken)}
                    onClick={{
                      top: processManager.evaluationClick,
                      down: processManager.evaluationClick
                    }}
                    text={{ top: idea.tokensSupport, down: idea.tokensOpposition }}
                    actions={getEvaluationActions(idea)}
                    active={idea.state.includes(STATE.idea.submittedSupport)}
                  />
                  : null}
                {site.examineIdeas && idea.state.includes(STATE.idea.examined)
                  ? <Examination message={idea.opinion} title={getExaminationTtile(idea)} value={getExaminationValue(idea)} />
                  : null}
                <Anchor
                  scrollEvent={scrollEvent}
                  getAnchor={() => {
                    return this.comments;
                  }}
                >
                  <Button variant="fab" color="primary" aria-label="comment" className={classes.goToComments}>
                    <Icon className={classNames(classes.goToCommentsIcon, 'mdi-set mdi-comment-outline')} />
                  </Button>
                </Anchor>
              </div>
              {hasEvaluation &&
                <div className={classes.right}>
                  <StatisticsDoughnut
                    classes={{
                      statisticsDoughnut: classes.statisticsDoughnut
                    }}
                    title="evaluation.tokens"
                    elements={stats}
                  />
                </div>}
              <h1
                ref={(title) => {
                  this.title = title;
                }}
                className={classes.title}
              >
                <IdeaIcon className={classes.icon} />
                {idea && idea.title}
              </h1>
              {images.length > 0 &&
                <div className={classes.imagesContainer}>
                  <ImagesPreview
                    images={images}
                    context={{
                      title: idea.title,
                      author: idea.author,
                      date: idea.createdAt
                    }}
                  />
                </div>}
              <MediumEditor readOnly value={idea.text} />
              <FilesPreview files={files} />
              <div
                ref={(comments) => {
                  this.comments = comments;
                }}
              >
                <Comments
                  rightDisabled
                  fullScreen
                  ignorDrawer
                  formTop
                  inline
                  channelId={idea.channel.id}
                  fetchMoreOnEvent={scrollEvent}
                  classes={{
                    container: classes.commentComntainer,
                    comments: classes.comments,
                    formContainer: classes.commentFormContainer,
                    list: classes.commentsList
                  }}
                />
              </div>
            </div>
          </Scrollbar>
          <Anchor
            scrollEvent={scrollEvent}
            getAnchor={() => {
              return this.title;
            }}
            classes={{ container: classes.goToTop }}
          >
            <Button variant="fab" color="primary" className={classes.goToTopBtn}>
              <Icon className={classNames(classes.goToTopIcon, 'mdi-set mdi-chevron-double-up')} />
            </Button>
          </Anchor>
        </div>
      </Dialog>
    );
  }
}

function IdeaWithProcessManager(props) {
  const { data, onActionClick } = props;
  return (
    <IdeaProcessManager idea={data.idea} onActionClick={onActionClick}>
      <DumbIdea {...props} />
    </IdeaProcessManager>
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
    graphql(Idea, {
      options: (props) => {
        return {
          fetchPolicy: 'cache-and-network',
          variables: {
            id: props.id || (props.params && props.params.ideaId),
            processIds: [],
            nodeIds: [],
            processTags: [],
            actionTags: [ACTIONS.primary]
          }
        };
      }
    })(IdeaWithProcessManager)
  )
);