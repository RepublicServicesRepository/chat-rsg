import { useTranslation } from 'react-i18next';
import Textarea from './Textarea';

export const Ideal = () => {
  const { t } = useTranslation();
  return (
    <Textarea
      label={t('feedbackDialog.commentLabel')}
      placeholder={t('feedbackDialog.commentPlaceholder')}
      hint={t('bot.help.instructions')}
      disabled={false}
      onChange={() => {}}
    />
  );
};

export const IdealDisabled = () => {
  const { t } = useTranslation();
  return (
    <Textarea
      label={t('feedbackDialog.commentLabel')}
      placeholder={t('feedbackDialog.commentPlaceholder')}
      hint={t('bot.help.instructions')}
      disabled={true}
      onChange={() => {}}
    />
  );
};

export const NoBorder = () => {
  const { t } = useTranslation();
  return (
    <Textarea
      label={t('feedbackDialog.commentLabel')}
      placeholder={t('feedbackDialog.commentPlaceholder')}
      hint={t('bot.help.instructions')}
      disabled={false}
      noBorder
      onChange={() => {}}
    />
  );
};

export const NoBorderDisabled = () => {
  const { t } = useTranslation();
  return (
    <Textarea
      label={t('feedbackDialog.commentLabel')}
      placeholder={t('feedbackDialog.commentPlaceholder')}
      hint={t('bot.help.instructions')}
      disabled={true}
      noBorder
      onChange={() => {}}
    />
  );
};
