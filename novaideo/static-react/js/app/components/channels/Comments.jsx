import React from 'react';
import { I18n } from 'react-redux-i18n';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import Grid from 'material-ui/Grid';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import debounce from 'lodash.debounce';

import { commentsQuery } from '../../graphql/queries';
import FlatList from '../common/FlatList';
import { filterActions } from '../../utils/processes';
import CommentItem from './CommentItem';
import CommentsFooter from './CommentsFooter';
import ChatAppRight from './chatAppRight/ChatAppRight';
import Divider from './Divider';
import Comment from '../forms/processes/common/Comment';
import { COMMENTS_ACTIONS, ACTIONS } from '../../processes';
import { markAsRead } from '../../graphql/processes/commentProcess';
import { markAsReadMutation } from '../../graphql/processes/commentProcess/markAsRead';

const styles = (theme) => {
  return {
    container: {
      height: 'calc(100vh - 56px)',
      position: 'relative'
    },
    comments: {
      backgroundColor: 'white',
      display: 'flex',
      justifyContent: 'space-between',
      flexDirection: 'column',
      height: '100%',
      position: 'relative'
    },
    commentsWithRight: {
      paddingRight: '0 !important',
      [theme.breakpoints.only('xs')]: {
        display: 'none'
      }
    },
    commentsWithRightFull: {
      display: 'none'
    },
    right: {
      backgroundColor: '#f9f9f9',
      borderLeft: '1px solid #e8e8e8',
      padding: '0 !important',
      paddingRight: '8px !important',
      paddingTop: '8px !important'
    },
    list: {
      height: 'calc(100% - 55px)'
    },
    header: {
      margin: '48px 32px 16px 16px',
      color: '#2c2d30',
      fontSize: 17,
      lineHeight: 1.5
    },
    noResult: {
      paddingLeft: 25,
      marginBottom: 15,
      fontSize: 15,
      color: '#717274',
      lineHeight: '20px'
    },
    blockComments: {
      position: 'absolute',
      bottom: 15,
      width: 'calc(100% - 49px)'
    }
  };
};

const NoComments = ({ classes }) => {
  return () => {
    return (
      <div className={classes.noResult}>
        {I18n.t('channels.noMessage')}
      </div>
    );
  };
};

const CtComment = ({ classes }) => {
  return () => {
    return (
      <div className={classes.noResult}>
        {I18n.t('channels.ctComment')}
      </div>
    );
  };
};

export class RenderComments extends React.Component {
  static defaultProps = {
    displayForm: true,
    dynamicDivider: true,
    displayFooter: true
  };

  componentDidUpdate() {
    const { data, markAsReadComments } = this.props;
    const channel = data.node;
    if (channel && channel.unreadComments && channel.unreadComments.length > 0) {
      debounce(() => {
        markAsReadComments({ context: channel, isDiscussion: channel.isDiscuss });
      }, 400)();
    }
  }

  render() {
    const {
      channelId,
      data,
      customScrollbar,
      dynamicDivider,
      reverted,
      inline,
      ignorDrawer,
      fullScreen,
      rightDisabled,
      rightOpen,
      rightFull,
      fetchMoreOnEvent,
      displayForm,
      formTop,
      formProps,
      classes,
      moreBtn,
      displayFooter,
      Footer,
      NoItems
    } = this.props;
    const channel = data.node;
    const subject = channel && channel.subject;
    const commentAction =
      displayForm && subject && subject.actions && filterActions(subject.actions, { behaviorId: COMMENTS_ACTIONS })[0];
    const contextOid = subject ? subject.oid : '';
    const displayRightBlock = !rightDisabled && rightOpen;
    const commentForm =
      commentAction &&
      <Comment
        key={channelId}
        form={channelId}
        channel={channel}
        context={contextOid}
        subject={contextOid}
        action={commentAction}
        {...formProps}
        classes={{ container: classNames(classes.formContainer, { [classes.blockComments]: !inline }) }}
      />;
    return (
      <Grid className={classes.container} container>
        <Grid
          className={classNames(classes.comments, {
            [classes.commentsWithRight]: displayRightBlock,
            [classes.commentsWithRightFull]: displayRightBlock && rightFull
          })}
          item
          xs={12}
          md={displayRightBlock ? 8 : 12}
          sm={displayRightBlock ? 7 : 12}
        >
          {formTop && commentForm}
          <FlatList
            Footer={displayFooter && (Footer || CommentsFooter)}
            NoItems={NoItems || (commentAction ? NoComments({ classes: classes }) : CtComment({ classes: classes }))}
            customScrollbar={customScrollbar}
            fetchMoreOnEvent={fetchMoreOnEvent}
            scrollEvent={channelId}
            reverted={reverted}
            onEndReachedThreshold={reverted ? 0.3 : 0.7}
            data={data}
            getEntities={(entities) => {
              return entities.node && entities.node.comments;
            }}
            ListItem={CommentItem}
            Divider={Divider}
            dividerProps={{
              fullScreen: fullScreen,
              ignorDrawer: ignorDrawer,
              dynamic: dynamicDivider
            }}
            itemProps={{
              channel: channel,
              inline: inline,
              unreadCommentsIds:
                channel && channel.unreadComments
                  ? channel.unreadComments.map((comment) => {
                    return comment.id;
                  })
                  : []
            }}
            moreBtn={moreBtn}
            className={classes.list}
          />
          {!formTop && commentForm}
        </Grid>
        {displayRightBlock && channel
          ? <Grid className={classes.right} item xs={12} md={rightFull ? 12 : 4} sm={rightFull ? 12 : 5}>
            <ChatAppRight channel={channel} />
          </Grid>
          : null}
      </Grid>
    );
  }
}

export const mapStateToProps = (state) => {
  return {
    rightOpen: state.apps.chatApp.right.open,
    rightFull: state.apps.chatApp.right.full
  };
};

export default withStyles(styles, { withTheme: true })(
  connect(mapStateToProps)(
    graphql(commentsQuery, {
      options: (props) => {
        return {
          fetchPolicy: 'cache-and-network',
          notifyOnNetworkStatusChange: true,
          variables: {
            filter: props.filter ? props.filter.text : '',
            pinned: props.filter ? !!props.filter.pinned : false,
            file: props.filter ? !!props.filter.file : false,
            first: 25,
            after: '',
            id: props.channelId,
            processIds: [],
            nodeIds: [],
            processTags: [],
            actionTags: [ACTIONS.primary],
            subjectActionsNodeIds: COMMENTS_ACTIONS
          }
        };
      }
    })(
      graphql(markAsReadMutation, {
        props: function (props) {
          return {
            markAsReadComments: markAsRead(props)
          };
        }
      })(RenderComments)
    )
  )
);