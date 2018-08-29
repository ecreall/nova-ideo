import React from 'react';
import { configure, addDecorator } from '@storybook/react';
import { setOptions } from '@storybook/addon-options';
import { I18n } from 'react-i18nify';
import centered from '@storybook/addon-centered'; // Library used to center H and V a component
import messages from '../js/app/utils/translations';

import '../css/novaideo.css';
import '../css/latofonts.css';

addDecorator(centered);

// Option defaults:
setOptions({
  name: 'Nova-Ideo',
  url: '#'
});

I18n.setTranslations(messages);
I18n.setLocale('fr');

function loadStories() {
  require('../js/app/integration/components/button.stories.jsx');
}

configure(loadStories, module);
