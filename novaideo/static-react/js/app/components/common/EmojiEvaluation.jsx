import React from 'react';
import classNames from 'classnames';
import { withStyles } from 'material-ui/styles';
import { Emoji } from 'emoji-mart';
import { Translate, I18n } from 'react-redux-i18n';
import { connect } from 'react-redux';

import EmojiPicker from '../forms/widgets/EmojiPicker';
import { PICKER_EMOJI_SHEET_APPLE_32 } from '../../constants';
import OverlaidTooltip from './OverlaidTooltip';

const styles = (theme) => {
  return {
    container: {
      display: 'flex',
      alignItems: 'center',
      marginTop: 5,
      marginBottom: 5,
      height: 30,
      '&:hover': {
        '& .emoji-picker-btn': {
          display: 'block'
        }
      }
    },
    count: {
      color: 'gray',
      fontSize: 12,
      padding: '0 1px 0 3px',
      position: 'relative'
    },
    emoji: {
      backgroundColor: 'rgba(78, 78, 78, 0.08)',
      border: '1px solid rgba(138, 138, 138, 0.4)',
      borderRadius: 3,
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '1px 3px',
      marginRight: 5,
      '&:hover': {
        border: '1px solid rgba(21, 110, 175, 1)'
      }
    },
    activeEmoji: {
      backgroundColor: 'rgba(21, 110, 175, 0.08)',
      border: 'solid 1px rgba(21, 110, 175, 0.4)',
      borderRadius: 3,
      '&:hover': {
        backgroundColor: 'rgba(21, 110, 175, 0.08)',
        border: '1px solid rgba(21, 110, 175, 1)'
      }
    },
    clicableEmoji: {
      cursor: 'pointer'
    },
    button: {
      display: 'none',
      height: 30,
      width: 30,
      '&:hover': {
        color: theme.palette.info[500]
      }
    },
    icon: {
      height: 20,
      width: 20
    },
    emojiTolltipTitle: {
      color: 'gray',
      marginLeft: 5
    }
  };
};

const EmojiTitle = ({ emoji, users, isUserEmoji, currentUser, classes }) => {
  const names = users
    .filter((user) => {
      return currentUser.id !== user.node.id;
    })
    .map((user) => {
      return user.node.title;
    });
  if (isUserEmoji) names.push(I18n.t('common.emojis.currentUserTooltip'));
  return (
    <span>
      {names.join(',')}
      <span className={classes.emojiTolltipTitle}>
        <Translate
          value={isUserEmoji ? 'common.emojis.currentTooltipTitle' : 'common.emojis.tooltipTitle'}
          count={users.length}
          emoji={emoji}
        />
      </span>
    </span>
  );
};

const EmojiEvaluation = ({ emojis, onEmojiClick, currentUser, classes }) => {
  if (emojis.length === 0) return null;
  let emojisContents = emojis.map((emoji) => {
    const count = emoji.users.totalCount;
    if (count === 0) return null;
    return (
      <OverlaidTooltip
        tooltip={
          <EmojiTitle
            classes={classes}
            emoji={emoji.title}
            users={emoji.users.edges}
            isUserEmoji={emoji.isUserEmoji}
            currentUser={currentUser}
          />
        }
        placement="top"
      >
        <div
          onClick={() => {
            if (onEmojiClick) onEmojiClick(emoji.title);
          }}
          className={classNames(classes.emoji, {
            [classes.activeEmoji]: emoji.isUserEmoji,
            [classes.clicableEmoji]: onEmojiClick
          })}
        >
          <span className={classes.count}>
            {count}
          </span>
          <Emoji
            sheetSize={32}
            backgroundImageFn={() => {
              return PICKER_EMOJI_SHEET_APPLE_32;
            }}
            emoji={emoji.title}
            size={18}
          />
        </div>
      </OverlaidTooltip>
    );
  });
  emojisContents = emojisContents.filter((emoji) => {
    return emoji;
  });
  if (emojisContents.length === 0) return null;
  return (
    <div className={classes.container}>
      {emojisContents}
      {onEmojiClick &&
        <EmojiPicker
          classes={{
            button: classNames('emoji-picker-btn', classes.button),
            icon: classes.icon
          }}
          onSelect={onEmojiClick}
          style={{ picker: { right: 1 } }}
        />}
    </div>
  );
};

export const mapStateToProps = (state) => {
  return {
    currentUser: state.globalProps.account
  };
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(EmojiEvaluation));