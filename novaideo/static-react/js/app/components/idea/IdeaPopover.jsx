/* eslint-disable react/no-array-index-key, no-undef */
import React from 'react';
import Moment from 'moment';
import { graphql } from 'react-apollo';
import { connect } from 'react-redux';
import Grid from 'material-ui/Grid';
import { I18n } from 'react-redux-i18n';
import Avatar from 'material-ui/Avatar';
import Tooltip from 'material-ui/Tooltip';
import { CardActions } from 'material-ui/Card';
import IconButton from 'material-ui/IconButton';
import Icon from 'material-ui/Icon';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import { CircularProgress } from 'material-ui/Progress';

import ImagesPreview from '../common/ImagesPreview';
import IconWithText from '../common/IconWithText';
import Evaluation from '../common/Evaluation';
import * as constants from '../../constants';
import { getActions } from '../../utils/entities';
import IdeaMenu from './IdeaMenu';
import IdeaActionsWrapper, { getEvaluationActions, getExaminationValue } from './IdeaActionsWrapper';
import { goTo, get } from '../../utils/routeMap';
import { closeChatApp } from '../../actions/actions';
import { ideaQuery } from '../../graphql/queries';
import Comment from '../forms/Comment';

const styles = (theme) => {
  return {
    ideaItem: {
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
      color: '#2c2d30',
      fontWeight: '900',
      justifyContent: 'space-around'
    },
    title: {
      '&:hover': {
        textDecoration: 'underline'
      }
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
    textContainer: {
      display: 'flex',
      justifyContent: 'space-between'
    },
    bodyFooter: {
      display: 'flex',
      flexDirection: 'row',
      marginTop: 10,
      marginBottom: 10
    },
    actionsContainer: {
      height: 0,
      width: '100%'
    },
    actionsText: {
      fontSize: 13,
      color: '#585858',
      fontWeight: '700',
      marginRight: 35,
      '&:hover': {
        color: theme.palette.info['700']
      }
    },
    actionsIcon: {
      fontWeight: 100,
      fontSize: '16px !important',
      marginRight: 5,
      marginTop: 1
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
      display: 'flex',
      justifyContent: 'center'
    },
    formContainer: {
      padding: 10,
      paddingRight: 10,
      paddingLeft: 10,
      backgroundColor: '#ededed',
      boxShadow: '0 -1px 0 rgba(0,0,0,.1)'
    }
  };
};

export class RenderIdeaItem extends React.Component {
  constructor(props) {
    super(props);
    this.menu = null;
  }

  onMouseOver = () => {
    if (this.menu) this.menu.open();
  };

  onMouseLeave = () => {
    if (this.menu) this.menu.close();
  };

  openDetails = () => {
    const { onActionClick } = this.props;
    if (onActionClick) onActionClick();
    this.props.closeChatApp();
    goTo(get('ideas', { ideaId: this.props.data.idea.id }));
  };

  onCommentSubmit = () => {
    const { onActionClick, data: { idea } } = this.props;
    if (onActionClick) onActionClick();
    setTimeout(() => {
      goTo(get('messages', { channelId: idea.channel.id }, { right: 'idea' }));
    }, 200);
  };

  render() {
    const { data, adapters, globalProps: { site }, classes } = this.props;
    if (data.loading) {
      return (
        <div className={classes.progress}>
          <CircularProgress size={30} />
        </div>
      );
    }
    const node = data.idea;
    const author = node.author;
    const authorPicture = author.picture;
    const isAnonymous = author.isAnonymous;
    const createdAt = Moment(node.createdAt).format(I18n.t('time.format'));
    const today = Moment();
    const isToday = today.isSame(Moment(node.createdAt), 'day');
    const yesterday = today.subtract(1, 'days').startOf('day');
    const isYesterday = yesterday.isSame(Moment(node.createdAt), 'day');
    const format = (isToday && 'date.todayFormat') || (isYesterday && 'date.yesterdayFormat') || 'date.format3';
    const createdAtF3 = Moment(node.createdAt).format(I18n.t(format));
    const images = node.attachedFiles
      ? node.attachedFiles.filter((image) => {
        return image.isImage;
      })
      : [];
    const hasEvaluation = site.supportIdeas && node.state.includes('published');
    const Examination = adapters.examination;
    const communicationActions = getActions(node.actions, constants.ACTIONS.communicationAction);
    const commentAction = node
      ? node.actions.filter((action) => {
        return action.behaviorId === 'comment';
      })[0]
      : null;
    return [
      <div className={classes.ideaItem} onMouseOver={this.onMouseOver} onMouseLeave={this.onMouseLeave}>
        <div className={classes.left}>
          <Avatar
            className={isAnonymous && classes.anonymousAvatar}
            classes={{ root: classes.avatar }}
            size={40}
            src={authorPicture ? `${authorPicture.url}/profil` : ''}
          >
            {isAnonymous && <Icon className={'mdi-set mdi-guy-fawkes-mask'} />}
          </Avatar>
          <div className={classes.leftActions}>
            {hasEvaluation
              ? <Evaluation
                icon={{
                  top:
                      node.userToken === 'support'
                        ? 'mdi-set mdi-arrow-up-drop-circle-outline'
                        : 'mdi-set mdi-arrow-up-drop-circle',
                  down:
                      node.userToken === 'oppose'
                        ? 'mdi-set mdi-arrow-down-drop-circle-outline'
                        : 'mdi-set mdi-arrow-down-drop-circle'
                }}
                onClick={{
                  top: (action) => {
                    this.props.actionsManager.evaluationClick(action);
                  },
                  down: (action) => {
                    this.props.actionsManager.evaluationClick(action);
                  }
                }}
                text={{ top: node.tokensSupport, down: node.tokensOpposition }}
                actions={getEvaluationActions(node)}
                active={node.state.includes('submitted_support')}
              />
              : null}
            {site.examineIdeas && node.state.includes('examined')
              ? <Examination title="Examination" message={node.opinion} value={getExaminationValue(node)} />
              : null}
          </div>
        </div>
        <div className={classes.body}>
          <div className={classes.header}>
            <IdeaMenu
              initRef={(menu) => {
                this.menu = menu;
              }}
              idea={node}
            />
            <span className={classes.headerTitle}>
              {author.title}
            </span>
            <Tooltip id={node.id} title={createdAtF3} placement="top">
              <span className={classes.headerAddOn}>
                {createdAt}
              </span>
            </Tooltip>
          </div>
          <div className={classes.bodyContent}>
            <div>
              <div className={classes.bodyTitle} onClick={this.openDetails}>
                <IconWithText name="mdi-set mdi-lightbulb" text={node.title} styleText={classes.title} />
              </div>

              <Grid container item>
                <Grid item xs={12} sm={!hasEvaluation && images.length > 0 ? 7 : 12}>
                  <div className={classes.ideaText} dangerouslySetInnerHTML={{ __html: node.presentationText }} />
                </Grid>
                {images.length > 0 &&
                  <Grid className={classes.imagesContainer} item xs={12} sm={hasEvaluation ? 8 : 5}>
                    <ImagesPreview images={images} />
                  </Grid>}
              </Grid>
            </div>
            <div className={classes.bodyFooter}>
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
          </div>
        </div>
      </div>,
      <Comment
        classes={{ container: classes.formContainer }}
        key={node.channel.id}
        form={node.channel.id}
        action={commentAction}
        context={node.oid}
        subject={node.oid}
        channel={node.channel}
        onSubmit={this.onCommentSubmit}
      />
    ];
  }
}

export const mapDispatchToProps = {
  closeChatApp: closeChatApp
};

export const mapStateToProps = (state) => {
  return {
    globalProps: state.globalProps,
    site: state.globalProps.site,
    adapters: state.adapters
  };
};

function DumbIdeaItem(props) {
  const { data, onActionClick } = props;
  return (
    <IdeaActionsWrapper idea={data.idea} onActionClick={onActionClick}>
      <RenderIdeaItem {...props} />
    </IdeaActionsWrapper>
  );
}

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