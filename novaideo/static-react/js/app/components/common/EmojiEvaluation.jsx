import React from 'react';
import classNames from 'classnames';
import { withStyles } from 'material-ui/styles';
import { Emoji } from 'emoji-mart';

import EmojiPicker from '../forms/widgets/EmojiPicker';
import { PICKER_EMOJI_SHEET_APPLE_32 } from '../../constants';

const styles = (theme) => {
  return {
    container: {
      display: 'flex',
      alignItems: 'center',
      marginTop: 5,
      marginBottom: 5
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
      marginRight: 5
    },
    activeEmoji: {
      backgroundColor: 'rgba(21, 110, 175, 0.08) !important',
      border: 'solid 1px rgba(21, 110, 175, 0.4) !important',
      borderRadius: 3
    },
    clicableEmoji: {
      cursor: 'pointer'
    },
    button: {
      height: 30,
      width: 30,
      '&:hover': {
        color: theme.palette.info[500]
      }
    },
    icon: {
      height: 20,
      width: 20
    }
  };
};

const EmojiEvaluation = ({ emojis, onEmojiClick, classes }) => {
  return (
    <div className={classes.container}>
      {emojis.map((emoji) => {
        const count = emoji.users.length;
        if (count === 0) return null;
        return (
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
        );
      })}
      {emojis.length > 0 &&
        onEmojiClick &&
        <EmojiPicker
          classes={{
            button: classes.button,
            icon: classes.icon
          }}
          onSelect={onEmojiClick}
          style={{ picker: { right: 1 } }}
        />}
    </div>
  );
};

export default withStyles(styles, { withTheme: true })(EmojiEvaluation);