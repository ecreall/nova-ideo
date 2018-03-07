/* eslint-disable react/no-array-index-key, no-undef */
import React from 'react';
import Moment from 'moment';
import { graphql } from 'react-apollo';
import { connect } from 'react-redux';
import Grid from 'material-ui/Grid';
import { I18n } from 'react-redux-i18n';
import Tooltip from 'material-ui/Tooltip';
import { withStyles } from 'material-ui/styles';
import { CircularProgress } from 'material-ui/Progress';

import ImagesPreview from '../common/ImagesPreview';
import IconWithText from '../common/IconWithText';
import Evaluation from '../common/Evaluation';
import AllignedActions from '../common/AllignedActions';
import { ACTIONS } from '../../processes';
import { getActions } from '../../utils/processes';
import { getFormattedDate } from '../../utils/globalFunctions';
import IdeaMenu from './IdeaMenu';
import IdeaProcessManager, { getEvaluationActions, getExaminationValue } from './IdeaProcessManager';
import { goTo, get } from '../../utils/routeMap';
import { closeChatApp } from '../../actions/actions';
import { ideaQuery } from '../../graphql/queries';
import UserAvatar from '../user/UserAvatar';

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
    minWidth: 320,
    minHeight: 340,
    display: 'flex',
    justifyContent: 'center'
  }
};

export class RenderIdeaItem extends React.Component {
  menu = null;

  onMouseOver = () => {
    if (this.menu) this.menu.open();
  };

  onMouseLeave = () => {
    if (this.menu) this.menu.close();
  };

  openDetails = () => {
    this.props.closeChatApp();
    this.props.processManager.onActionPerformed();
    goTo(get('ideas', { ideaId: this.props.data.idea.id }));
  };

  render() {
    const { data, adapters, globalProps: { site }, classes } = this.props;
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
    const createdAt = Moment(node.createdAt).format(I18n.t('time.format'));
    const createdAtF3 = getFormattedDate(node.createdAt, 'date.format3');
    const images = node.attachedFiles
      ? node.attachedFiles.filter((image) => {
        return image.isImage;
      })
      : [];
    const state = node.state || [];
    const hasEvaluation = site.supportIdeas && state.includes('published');
    const Examination = adapters.examination;
    const communicationActions = getActions(node.actions, { tags: ACTIONS.communication });
    return (
      <div className={classes.container} onMouseOver={this.onMouseOver} onMouseLeave={this.onMouseLeave}>
        <div className={classes.left}>
          <UserAvatar isAnonymous={isAnonymous} picture={authorPicture} title={author.title} />
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
                  top: this.props.processManager.evaluationClick,
                  down: this.props.processManager.evaluationClick
                }}
                text={{ top: node.tokensSupport, down: node.tokensOpposition }}
                actions={getEvaluationActions(node)}
                active={state.includes('submitted_support')}
              />
              : null}
            {site.examineIdeas && state.includes('examined')
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
              onActionClick={this.props.processManager.performAction}
            />
            <span className={classes.headerTitle}>
              {author && author.title}
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
              <AllignedActions actions={communicationActions} onActionClick={this.props.processManager.performAction} />
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
    site: state.globalProps.site,
    adapters: state.adapters
  };
};

function DumbIdeaItem(props) {
  const { data, onActionClick } = props;
  return (
    <IdeaProcessManager idea={data.idea} onActionClick={onActionClick}>
      <RenderIdeaItem {...props} />
    </IdeaProcessManager>
  );
}

export default withStyles(styles)(
  connect(mapStateToProps, mapDispatchToProps)(
    graphql(ideaQuery, {
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
    })(DumbIdeaItem)
  )
);