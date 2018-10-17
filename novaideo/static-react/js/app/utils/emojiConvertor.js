import { EmojiConvertor } from 'emoji-js';

import { PICKER_EMOJI_SHEET_APPLE_32 } from '../constants';

function getNewEmojiConvertor() {
  const emoji = new EmojiConvertor();
  const emojiUrl = PICKER_EMOJI_SHEET_APPLE_32;
  emoji.img_sets = {
    apple: {
      path: emojiUrl,
      sheet: emojiUrl,
      sheet_size: 32,
      mask: 1
    }
  };
  emoji.use_sheet = true;
  emoji.init_env();
  emoji.img_set = 'apple';
  emoji.text_mode = false;
  emoji.include_title = true;
  return emoji;
}

const emojiConvertor = getNewEmojiConvertor();

export function emojiConvert(text) {
  return emojiConvertor.replace_unified(emojiConvertor.replace_emoticons(text));
}