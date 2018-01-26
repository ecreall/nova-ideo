import { ShortcutManager } from 'react-shortcuts';

const keymap = {
  APP: {
    CHATAPP_OPEN_JUMP: ['ctrl+k'],
    CHATAPP_CLOSE: ['escape'],
    CHATAPP_INFO: ['ctrl+i']
  }
};

const shortcutManager = new ShortcutManager(keymap);
export default shortcutManager;