/* eslint-disable react/no-array-index-key, no-undef */
import React from 'react';
import Moment from 'moment';
import { connect } from 'react-redux';
import { I18n } from 'react-redux-i18n';
import Tooltip from '@material-ui/core/Tooltip';
import { withStyles } from '@material-ui/core/styles';
import Icon from '@material-ui/core/Icon';
import classNames from 'classnames';
import * as Vibrant from 'node-vibrant';

import ImagesPreview from '../common/ImagesPreview';
import Keywords from '../common/Keywords';
import IconWithText from '../common/IconWithText';
import Evaluation from '../common/Evaluation';
import AllignedActions from '../common/AllignedActions';
import StatisticsDoughnut from '../common/Doughnut';
import { getActions } from '../../utils/processes';
import { getFormattedDate } from '../../utils/globalFunctions';
import OverlaidTooltip from '../common/OverlaidTooltip';
import { goTo, get } from '../../utils/routeMap';
import { ACTIONS, PROCESSES, STATE } from '../../processes';
import IdeaMenu from './IdeaMenu';
import IdeaProcessManager from './IdeaProcessManager';
import { closeChatApp } from '../../actions/chatAppActions';
import UserTitle from '../user/UserTitle';
import UserAvatar from '../user/UserAvatar';
import {
  getEvaluationIcons, getEvaluationActions, getExaminationValue, getIdeaSupportStats, getExaminationTtile
} from '.';

const styles = (theme) => {
  return {
    container: {
      display: 'flex',
      position: 'relative',
      padding: '15px 12px',
      '&:hover': {
        backgroundColor: '#f9f9f9'
      }
    },
    privateContainer: {
      backgroundColor: `rgba(${Vibrant.Util.hexToRgb(theme.palette.primary[500]).join(',')}, 0.07)`
    },
    header: {
      display: 'flex',
      flexDirection: 'row',
      alignItems: 'center',
      margin: '10px 0',
      position: 'relative'
    },
    headerTitle: {
      color: '#737373',
      fontWeight: 'bold'
    },
    title: {
      color: '#2c2d30',
      fontSize: 17,
      fontWeight: 900
    },
    activeTitle: {
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
      width: '100%',
      paddingRight: 7
    },
    bodyTitle: {
      marginLeft: -3,
      marginBottom: 10,
      cursor: 'pointer'
    },
    disableBodyTitle: {
      cursor: 'inherit'
    },
    left: {
      display: 'flex',
      alignItems: 'center',
      paddingRight: 10,
      margin: '8px 0',
      flexDirection: 'column'
    },
    right: {
      backgroundColor: '#f5f5f5',
      marginTop: -15,
      marginBottom: -15,
      marginRight: -12
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
    bodyFooter: {
      display: 'flex',
      flexDirection: 'row',
      marginTop: 10,
      marginBottom: 10
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
      lineHeight: '20px',
      whiteSpace: 'pre-wrap',
      wordWrap: 'break-word',
      cursor: 'pointer',
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
      padding: '0 0 0 8px !important',
      maxWidth: 460
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
    }
  };
};

export class DumbIdeaItem extends React.Component {
  static defaultProps = {
    passive: false,
    itemProps: { withStatic: true }
  };

  menu = null;

  onMouseOver = () => {
    if (this.menu) this.menu.open();
  };

  onMouseLeave = () => {
    if (this.menu) this.menu.close();
  };

  openDetails = () => {
    const { channelOpen, node: { id } } = this.props;
    if (id !== '0') {
      if (channelOpen) {
        this.props.closeChatApp();
      }
      goTo(get('ideas', { ideaId: id }));
    }
  };

  render() {
    const {
      node, processManager, passive, adapters, itemProps: { withStatic }, globalProps: { site }, classes
    } = this.props;

    const { author } = node;
    const { isAnonymous, title, picture } = author;
    const createdAt = Moment(node.createdAt).format(I18n.t('time.format'));
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
    const publishAction = !passive && isPrevate && getActions(node.actions, { nodeId: ideaProcessNodes.publish.nodeId })[0];
    const Examination = adapters.examination;
    const onIdeaClick = !passive ? this.openDetails : null;
    return (
      <div
        className={classNames(classes.container, { [classes.privateContainer]: isPrevate })}
        onMouseOver={this.onMouseOver}
        onMouseLeave={this.onMouseLeave}
      >
        <div className={classes.left}>
          <UserAvatar isAnonymous={isAnonymous} picture={picture} title={title} />
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
                active={node.state.includes(STATE.idea.submittedSupport)}
              />
            ) : null}
            {site.examineIdeas && node.state.includes(STATE.idea.examined) ? (
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
            {!passive && (
              <IdeaMenu
                initRef={(menu) => {
                  this.menu = menu;
                }}
                idea={node}
                onActionClick={processManager.execute}
              />
            )}
            <UserTitle node={author} classes={{ title: classes.headerTitle }} />
            {node.keywords.length > 0 && <Keywords onKeywordPress={this.props.searchEntities} keywords={node.keywords} />}
            <Tooltip id={node.id} title={createdAtF3} placement="top">
              <span className={classes.headerAddOn}>{createdAt}</span>
            </Tooltip>
          </div>
          <div className={classes.bodyContent}>
            <div>
              <div className={classNames(classes.bodyTitle, { [classes.disableBodyTitle]: passive })} onClick={onIdeaClick}>
                <IconWithText
                  name="mdi-set mdi-lightbulb"
                  text={node.title}
                  styleText={classNames(classes.title, { [classes.activeTitle]: !passive })}
                  styleIcon={classes.icon}
                />
              </div>
              <div>
                <div
                  onClick={onIdeaClick}
                  className={classes.ideaText}
                  dangerouslySetInnerHTML={{ __html: node.presentationText }}
                />
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
              {!passive && (
                <AllignedActions actionDecoration actions={communicationActions} onActionClick={processManager.execute} />
              )}
            </div>
          </div>
        </div>
        {withStatic
          && hasEvaluation && (
          <div className={classes.right}>
            <StatisticsDoughnut title="evaluation.tokens" elements={getIdeaSupportStats(node, classes)} />
          </div>
        )}
      </div>
    );
  }
}

function IdeaItemWithProcessManager(props) {
  const { node, onActionClick } = props;
  return (
    <IdeaProcessManager idea={node} onActionClick={onActionClick}>
      <DumbIdeaItem {...props} />
    </IdeaProcessManager>
  );
}

export const mapDispatchToProps = {
  closeChatApp: closeChatApp
};

export const mapStateToProps = (state) => {
  return {
    globalProps: state.globalProps,
    adapters: state.adapters,
    channelOpen: state.apps.chatApp.open
  };
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps, mapDispatchToProps)(IdeaItemWithProcessManager));