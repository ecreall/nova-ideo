/* eslint-disable react/no-array-index-key, no-undef */
import React from 'react';
import Moment from 'moment';
import { graphql } from 'react-apollo';
import { connect } from 'react-redux';
import { I18n } from 'react-redux-i18n';
import Tooltip from '@material-ui/core/Tooltip';
import { withStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';
import Icon from '@material-ui/core/Icon';
import classNames from 'classnames';

import OverlaidTooltip from '../common/OverlaidTooltip';
import ImagesPreview from '../common/ImagesPreview';
import IconWithText from '../common/IconWithText';
import Evaluation from '../common/Evaluation';
import AllignedActions from '../common/AllignedActions';
import { ACTIONS, PROCESSES, STATE } from '../../processes';
import { getActions } from '../../utils/processes';
import { getFormattedDate } from '../../utils/globalFunctions';
import IdeaMenu from './IdeaMenu';
import IdeaProcessManager from './IdeaProcessManager';
import { goTo, get } from '../../utils/routeMap';
import { closeChatApp } from '../../actions/chatAppActions';
import Idea from '../../graphql/queries/Idea.graphql';
import UserAvatar from '../user/UserAvatar';
import { getEvaluationIcons, getEvaluationActions, getExaminationValue, getExaminationTtile } from '.';

const styles = {
  container: {
    display: 'flex',
    position: 'relative',
    padding: '15px 12px',
    minWidth: 320,
    maxWidth: 450,
    marginBottom: 5,
    '&:hover': {
      backgroundColor: '#f9f9f9'
    }
  },
  header: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    margin: '10px 0',
    position: 'relative'
  },
  headerTitle: {
    display: 'flex',
    fontSize: 15,
    color: '#737373',
    fontWeight: '900',
    justifyContent: 'space-around'
  },
  title: {
    color: '#2c2d30',
    fontSize: 17,
    fontWeight: 900,
    '&:hover': {
      textDecoration: 'underline'
    }
  },
  icon: {
    color: '#2c2d30',
    fontSize: '16px !important',
    marginRight: 3
  },
  headerAddOn: {
    color: '#999999ff',
    paddingLeft: 5,
    fontSize: 13
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
    height: '100%',
    marginTop: 15
  },
  bodyFooter: {
    display: 'flex',
    flexDirection: 'row',
    marginTop: 15,
    marginBottom: 5
  },
  ideaText: {
    lineHeight: '20px',
    whiteSpace: 'pre-wrap',
    wordWrap: 'break-word',
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
    padding: '0 0 0 8px !important'
  },
  progress: {
    width: '100%',
    minWidth: 320,
    minHeight: 340,
    display: 'flex',
    justifyContent: 'center'
  },
  iconPrivate: {
    fontSize: '30px !important',
    color: '#607D8B',
    textShadow: '0 1px 3px rgba(128, 128, 128, 0.7)'
  },
  iconActive: {
    cursor: 'pointer',
    '&:hover': {
      color: '#3c525d'
    }
  },
  actionsContainer: {
    justifyContent: 'center'
  }
};

export class DumbIdeaPopover extends React.Component {
  menu = null;

  onMouseOver = () => {
    if (this.menu) this.menu.open();
  };

  onMouseLeave = () => {
    if (this.menu) this.menu.close();
  };

  openDetails = () => {
    this.props.closeChatApp();
    this.props.processManager.onActionExecuted();
    goTo(get('ideas', { ideaId: this.props.data.idea.id }));
  };

  render() {
    const {
      data,
      processManager,
      adapters,
      globalProps: { site },
      classes
    } = this.props;
    const node = data.idea;
    if (!node || !node.author) {
      return (
        <div className={classes.progress}>
          <CircularProgress size={30} />
        </div>
      );
    }
    const author = node.author;
    const authorPicture = author.picture;
    const isAnonymous = author.isAnonymous;
    const createdAt = Moment(node.createdAt).format(I18n.t('date.format'));
    const createdAtF3 = getFormattedDate(node.createdAt, 'date.format3');
    const images = node.attachedFiles
      ? node.attachedFiles.filter((image) => {
        return image.isImage;
      })
      : [];
    const state = node.state || [];
    const hasEvaluation = site.supportIdeas && state.includes(STATE.idea.published);
    const isPrevate = state.includes(STATE.idea.private);
    const ideaProcessNodes = PROCESSES.ideamanagement.nodes;
    const communicationActions = getActions(node.actions, { tags: ACTIONS.communication });
    const publishAction = isPrevate && getActions(node.actions, { nodeId: ideaProcessNodes.publish.nodeId })[0];
    const Examination = adapters.examination;
    return (
      <div className={classes.container} onMouseOver={this.onMouseOver} onMouseLeave={this.onMouseLeave}>
        <div className={classes.left}>
          <UserAvatar isAnonymous={isAnonymous} picture={authorPicture} title={author.title} />
          <div className={classes.leftActions}>
            {hasEvaluation ? (
              <Evaluation
                icon={getEvaluationIcons(node.userToken)}
                onClick={{
                  top: processManager.evaluationClick,
                  down: processManager.evaluationClick
                }}
                text={{ top: node.tokensSupport, down: node.tokensOpposition }}
                actions={getEvaluationActions(node)}
                active={state.includes(STATE.idea.submittedSupport)}
              />
            ) : null}
            {site.examineIdeas && state.includes(STATE.idea.examined) ? (
              <Examination message={node.opinion} title={getExaminationTtile(node)} value={getExaminationValue(node)} />
            ) : null}
            {isPrevate && (
              <OverlaidTooltip
                tooltip={publishAction ? I18n.t('idea.privatePublishAction') : I18n.t('idea.private')}
                placement="top"
              >
                <Icon
                  className={classNames('mdi-set mdi-lock', classes.iconPrivate, { [classes.iconActive]: publishAction })}
                  onClick={
                    publishAction
                      ? () => {
                        processManager.execute(publishAction);
                      }
                      : null
                  }
                />
              </OverlaidTooltip>
            )}
          </div>
        </div>
        <div className={classes.body}>
          <div className={classes.header}>
            <IdeaMenu open idea={node} onActionClick={processManager.execute} />
            <span className={classes.headerTitle}>{author && author.title}</span>
            <Tooltip id={node.id} title={createdAtF3} placement="top">
              <span className={classes.headerAddOn}>{createdAt}</span>
            </Tooltip>
          </div>
          <div className={classes.bodyContent}>
            <div>
              <div className={classes.bodyTitle} onClick={this.openDetails}>
                <IconWithText name="mdi-set mdi-lightbulb" text={node.title} styleText={classes.title} styleIcon={classes.icon} />
              </div>
              <div>
                <div className={classes.ideaText} dangerouslySetInnerHTML={{ __html: node.presentationText }} />
                {images.length > 0 && (
                  <div className={classes.imagesContainer}>
                    <ImagesPreview
                      images={images}
                      context={{
                        title: node.title,
                        author: author,
                        date: node.createdAt
                      }}
                    />
                  </div>
                )}
              </div>
            </div>
            <div className={classes.bodyFooter}>
              <AllignedActions
                actionDecoration
                actions={communicationActions}
                onActionClick={processManager.execute}
                classes={{ actionsContainer: classes.actionsContainer }}
              />
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export const mapDispatchToProps = {
  closeChatApp: closeChatApp
};

export const mapStateToProps = (state) => {
  return {
    globalProps: state.globalProps,
    adapters: state.adapters
  };
};

function IdeaPopoverWithProcessManager(props) {
  const { data, onActionClick, onFormOpened, onFormClosed } = props;
  return (
    <IdeaProcessManager idea={data.idea} onActionClick={onActionClick} onFormOpened={onFormOpened} onFormClosed={onFormClosed}>
      <DumbIdeaPopover {...props} />
    </IdeaProcessManager>
  );
}

export default withStyles(styles)(
  connect(
    mapStateToProps,
    mapDispatchToProps
  )(
    graphql(Idea, {
      options: (props) => {
        return {
          fetchPolicy: 'cache-and-network',
          variables: {
            id: props.id,
            processIds: [],
            nodeIds: [],
            processTags: [],
            actionTags: [ACTIONS.primary]
          }
        };
      }
    })(IdeaPopoverWithProcessManager)
  )
);