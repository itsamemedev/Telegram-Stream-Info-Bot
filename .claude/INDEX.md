# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 10637  GET              /                                                dashboard
 12694  GET              /api/abo/status                                  api_abo_status
 12648  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11425  GET              /api/automation/status                           api_automation_status
 11447  POST             /api/automation/toggle                           api_automation_toggle
 20987  GET              /api/channel/categories                          api_channel_categories
 20993  POST             /api/channel/set                                 api_channel_set
 20840  GET              /api/channels/status                             api_channels_status
 20514  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20497  GET              /api/clips                                       api_clips
 20543  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20415  GET              /api/debug/threads                               api_debug_threads
 12659  GET              /api/events                                      api_events
 12138  GET              /api/events/stream                               api_events_stream
 11965  GET              /api/health                                      api_health
 20456  POST             /api/highlights/config                           api_highlights_config
 10567  POST             /api/login                                       dashboard_login_submit
 12984  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12053  GET              /api/notify/status                               api_notify_status
 12064  POST             /api/notify/test                                 api_notify_test
 12748  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12725  GET              /api/proxy/trend                                 api_proxy_trend
 20563  GET              /api/tts/<fn>                                    api_tts_file
 21337  GET              /api/upload_window                               api_upload_window
 12255  GET              /archive/<int:eid>/download                      archive_download
 12283  GET              /download/<int:recording_id>                     download
 12212  GET              /health                                          health
 20324  GET              /healthz                                         healthz
 10558  GET              /login                                           dashboard_login_page
 10592  GET              /logout                                          dashboard_logout
 10599  GET              /manifest.webmanifest                            pwa_manifest
 21310  GET              /overlay                                         overlay_page
 10623  GET              /pwa-icon-<variant>.png                          pwa_icon
 10609  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (345)

```
   195  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   422  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   993  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   738  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   864  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   844  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   882  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   806  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   546  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   644  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1231  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1263  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   341  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   946  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   926  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1099  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1147  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1198  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1057  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   901  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   504  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   768  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   650  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   633  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   625  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   812  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   777  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   797  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   684  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   238  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   263  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   268  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   406  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   397  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   343  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   230  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   196  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   179  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   399  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   532  GET              /api/beobachtung/dienste                         api_beobachtung_dienste   [nc/routes/beobachtung.py]
   525  GET              /api/beobachtung/lage                            api_beobachtung_lage   [nc/routes/beobachtung.py]
   547  POST             /api/beobachtung/steuern                         api_beobachtung_steuern   [nc/routes/beobachtung.py]
   376  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   174  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   443  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   433  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   418  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   238  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   195  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    73  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    80  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   497  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   259  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   286  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   379  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   323  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   341  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   246  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   112  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   120  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   136  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
    56  GET              /api/einstellungen                               api_einstellungen   [nc/routes/einstellungen.py]
    68  POST             /api/einstellungen                               api_einstellungen_setzen   [nc/routes/einstellungen.py]
   102  POST             /api/einstellungen/uebernehmen                   api_einstellungen_uebernehmen   [nc/routes/einstellungen.py]
    86  POST             /api/einstellungen/zuruecksetzen                 api_einstellungen_zuruecksetzen   [nc/routes/einstellungen.py]
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   204  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   224  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   251  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   394  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   297  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   414  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   409  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   485  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   307  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   222  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   244  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   171  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   149  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   128  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   178  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
    66  GET              /api/lagebild                                    api_lagebild   [nc/routes/lagebild.py]
   428  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   257  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   324  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   352  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   203  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   270  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   505  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   168  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   151  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   391  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   238  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   227  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   210  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
   119  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   268  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   590  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   565  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   974  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1096  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1124  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1144  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   961  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1023  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1010  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   991  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   636  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   631  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   679  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   562  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   889  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   653  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   616  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   589  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   863  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   733  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   822  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   728  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   661  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   441  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   906  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   529  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   784  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   939  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   924  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   485  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   723  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   709  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   692  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   749  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1287  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1408  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1251  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   842  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   738  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   490  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   468  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   509  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   526  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   578  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   444  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   600  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   539  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   565  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   148  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   160  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   474  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   464  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   499  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   366  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   456  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   578  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   397  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   427  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   219  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    74  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   118  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   141  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   105  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   375  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   389  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   189  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   237  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   458  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   487  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   407  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   420  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   516  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   393  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   268  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   337  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   324  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   164  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   282  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   133  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   374  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   429  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   265  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   453  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   419  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   478  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   458  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   441  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   434  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   251  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   317  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
    73  GET              /fonts/<name>                                    schrift   [nc/routes/schriften.py]
    66  GET              /fonts/schriften.css                             schriften_css   [nc/routes/schriften.py]
   469  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (67)

```
  2256  /about                  Ueber diesen Bot
   961  /ai                     
  2256  /aireset                KI-Kontext zuruecksetzen
  1375  /ask                    
  1062  /assign_role            
  1112  /ban                    
  2211  /botstats               
  2256  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2256  /bulkadd                Mehrere User auf einmal tracken · a b c
  2256  /cleanup                Alte Aufnahmen aufraeumen
  1641  /clearwarns             
  2175  /clip                   
  2160  /clipoftheweek          
  1511  /clips                  
  2256  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1017  /create_category        
   988  /create_channel         
  1052  /create_group           
  1027  /create_role            
  1003  /create_voice           
  1253  /daily                  
  2256  /diag                   Vollstaendige Diagnose
  2256  /einnahmen              Einnahmen und Spenden
  1404  /event                  
  1446  /events                 
  1551  /follow                 
  1540  /help                   
  1102  /kick                   
  1228  /leaderboard            
  2256  /live                   Live-Status sofort pruefen · @user
  1498  /livenow                
  2256  /logs                   Letzte Fehler aus dem Log
  2256  /pause                  Tracking pausieren · @user
  1526  /post_test              
  1336  /profile                
  1134  /purge                  
  2256  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2256  /quota                  Speicher-Quota
  1215  /rank                   
  1486  /recstatus              
  1072  /remove_role            
  2256  /report                 Azrael-Sentinel-Wochenreport
   974  /restream_status        
  2256  /resume                 Tracking fortsetzen · @user
  1082  /set_channel_perms      
  1177  /setup_community        
  1194  /setup_targets          
  1472  /spenden                
  1583  /stats                  
   933  /status                 
  2256  /stoprec                Laufende Aufnahme sauber beenden · @user
  1679  /streaminfo             
  2256  /summary                Tageszusammenfassung
  2256  /sysres                 System-Ressourcen
  2256  /teststream             Recorder-Selbsttest · @user
  2256  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1122  /timeout                
  1651  /topstreamers           
  2256  /topusers               Top-Streamer nach Aufnahmen
   863  /track                  
  2256  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   946  /tracklist              
  1565  /unfollow               
  2256  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   895  /untrack                
  1604  /warn                   
  1627  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2419  on_member_join
  2376  on_message
  2277  on_raw_reaction_add
  2454  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-490    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (54 Funktionen)

```
  1756-1807   _award_xp
   535-562    _bereich_umziehen
   482-492    _clip_kopieren
  1978-2007   _clip_week_leader
  2031-2045   _clipoftheweek_loop
  2571-2633   _community_events_loop
  1713-1735   _dc_client
  1738-1747   _dc_offen
  2673-2708   _disc_automod_check
   408-413    _disc_sprache_setzen
  1810-1858   _discord_ai_automod
   684-723    _discord_automod
  1861-1881   _discord_azrael_reply
  2048-2530   _discord_run_once
   243-301    _discord_start
   304-358    _ensure_discord_invite
  2536-2568   _ensure_error_channel
   429-442    _ensure_rank_roles
   826-840    _ensure_team_roles
  2636-2666   _error_channel_loop
   733-737    _guard
   653-681    _handle_voice_ai
   416-426    _is_admin
   507-532    _link_video
  1926-1937   _liveboard_loop
   740-758    _on_level_up
   649-650    _par_chat_id
  2010-2028   _post_clip_of_week
  1940-1958   _post_weekly_digest
   445-471    _provision_base_channels
  1478-1572   _reg_betrieb
  1148-1242   _reg_community_setup
  1245-1325   _reg_daily_profil
  1368-1465   _reg_frage_events
   920-976    _reg_info
  1094-1145   _reg_moderation
  1328-1365   _reg_profil
  1043-1091   _reg_rollen
   979-1040   _reg_server
  1468-1475   _reg_spenden
  1575-1662   _reg_streamer
  1665-1710   _reg_system
   854-917    _reg_tracking
   793-823    _run_tg_handler
   636-646    _tracked_usernames
   160-222    _uebernehmen
   495-504    _umzugsmarken
  1890-1923   _update_liveboard
  1961-1975   _weekly_digest_loop
   474-479    _ziel_guild
   565-607    _ziele_abgleichen
   616-633    _ziele_sync_loop
   610-613    _ziele_takt_min
   225-228    starte
```

## Top-Level-Symbole in bot.py (577 Funktionen, 3 Klassen)

```
 26325-26347  _abbruch_datenbank_unlesbar
  2742-2743   _abo_key
  2763-2781   _abo_probe_dump
 26443-26459  _abschied_wachen
 26462-26480  _abschluss
 16647-16654  _ad_allowlist
 17781-17787  _agent_for
 17790-17806  _ai_telemetry
 18303-18321  _alert
 22205-22255  _alert_monitor_loop
 18982-19039  _alte_beilagen_einsammeln
 22637-22699  _announce_loop
  3638-3648   _anthropic_key
  3655-3657   _anthropic_model
 10222-10225  _arg_int
  2734-2739   _as_dict
 26011-26020  _async_exc_handler
 18484-18506  _audio_tap_cmd
 19490-19549  _audio_tap_melden
 18520-18544  _audio_tap_sammler
  9567-9604   _aufnahme_beim_stopp_sichern
 18924-18945  _aufnahme_chat_ausklang
 18908-18921  _aufnahme_chat_beginnen
 19067-19088  _aufnahme_chat_dienst
 19259-19309  _aufnahme_chat_einarbeiten
 18903-18905  _aufnahme_chat_modus
 19091-19140  _aufnahme_chat_nachtrag
 18948-18979  _aufnahme_chat_vormerken
 19058-19064  _aufnahme_chat_wecken
 25260-25262  _aufnahme_deckel
 19143-19164  _aufnahme_fertigmachen
  9607-9625   _aufnahme_platz_frei
 26407-26427  _aufnahmen_abschliessen
 26350-26404  _aufraeumen
 10421-10490  _auth_cookie
 10379-10417  _auth_guard
  1983-1988   _auto_on
 20176-20194  _auto_restream_loop
 14269-14311  _avatar_frames_laden
 23772-23787  _azrael_broadcast_reply
 23672-23694  _azrael_chat_reply
 23644-23669  _azrael_chat_should_reply
 23700-23702  _azrael_gate_cfg
 17811-17825  _azrael_live_state
 21223-21237  _azrael_overlay_state
 18185-18239  _azrael_proactive_loop
 17629-17685  _azrael_reaction_to_chats
 23705-23712  _azrael_reply_all_chats
 23631-23641  _azrael_self_names
 23740-23769  _azrael_send_to
 14230-14266  _azrael_spricht
 14573-14586  _azrael_stimme_stumm
 17831-17852  _azrael_system
 22339-22342  _backup_active
 22420-22433  _backup_loop
 25349-25353  _betrieb
 26084-26093  _brain_crowdsec_snap
 26252-26255  _brain_db_health
 22126-22135  _brain_growth_loop
 10816-10843  _brain_growth_snapshot
  2667-2687   _brain_hint_delay
 26156-26191  _brain_moderation_snap
  6584-6612   _brain_notify
 26258-26280  _brain_recording_snap
 26096-26153  _brain_restream_health
 26283-26296  _brain_tiktok_status_snap
 12117-12134  _browser_push
  6624-6711   _build_daily_summary
 14620-14624  _build_restream_cmd
  5337-5364   _can_stop_tracking
  2096-2118   _capture_set_cookies
 12802-12805  _cfg_get
 12808-12810  _cfg_set
 20948-20983  _channel_set_all
 13381-13384  _chat_connected
 13387-13403  _chat_disconnected
 19052-19055  _chat_einarbeiten_async
  9082-9093   _chat_is_forum
 18872-18897  _chat_listener_abbauen
 13423-13425  _chat_sanitize
 13366-13378  _chat_stat
 13406-13409  _chat_stats_snapshot
  3956-3968   _check_ai_models_sync
 11098-11141  _classify_pool_anonymity
 11144-11161  _classify_pool_anonymity_bg
   900-922    _claude_chat_sync_metered
 10254-10260  _client_ip
 23271-23285  _clip_chat_ass
 22783-22817  _clip_prune
 22820-22830  _clip_recfile_for
 23194-23259  _clip_schneiden
 23288-23294  _clip_should_velocity
 22872-22957  _clip_to_discord
 19230-19235  _clips_abwarten
  3842-3851   _close_ai_session
 23818-23833  _cohost_broadcast
 23803-23804  _cohost_cfg
 23859-23871  _cohost_fire_highlight
 23807-23815  _cohost_gate
 23836-23856  _cohost_highlight
 10746-10748  _conv_messages
  6983-7044   _cookie_alarm_loop
  2186-2187   _cookie_autofetch_info
  2170-2174   _cookie_autorefresh_info
 25718-25740  _cookie_bezug_loop
 25743-25768  _cookie_bezug_runde
  2073-2077   _cookie_header
 10263-10268  _cookie_sicher
  2199-2213   _cookies_selbst_holen
  4172-4174   _create_index_safe
 21669-21783  _crowdsec_status
 21615-21666  _crowdsec_via_lapi
 21519-21537  _cscli_bin
 21546-21559  _cscli_path
  6873-6898   _daily_summary_loop
 21577-21594  _darf_journal_lesen
  3167-3192   _darf_ytdlp_nachschlagen
 12298-12319  _dashboard_adresse
  1481-1511   _dashboard_trackings_umziehen
 23262-23268  _datei_weg
 22179-22202  _db_maintenance_loop
  6842-6870   _db_vacuum_loop
 16670-16694  _detect_foreign_ad
  1663-1674   _diag_path_owner
 18090-18135  _director_finalize
 19479-19486  _director_for
 18039-18087  _director_mark
 23107-23110  _disc_state_get
 23113-23120  _disc_state_set
 22107-22116  _discord_bot_starten
 22070-22081  _discord_einladung_merken
 22119-22123  _discord_invite
 22084-22104  _discord_kontext
 23068-23104  _discord_live_thread
 18242-18254  _discord_notify
 22042-22067  _discord_ops_alert
 22968-23064  _discord_post_user
 22702-22708  _discord_stop
  6901-6978   _disk_alarm_loop
 25643-25692  _disk_autoclean
 25866-25879  _disk_guard_loop
 14208-14215  _drossel_hoeher
 14204-14205  _drossel_stufe
 14218-14226  _drossel_zuruecksetzen
 12475-12477  _dump_all_threads
 25356-25370  _einstellungen_startzeile
 11024-11087  _enrich_proxies_with_geo
  2242-2303   _ensure_cookie_file_netscape
  9255-9258   _ensure_notify_topic
 11268-11305  _ensure_proxy_ready
  9109-9131   _ensure_topic
   743-745    _env_int
   748-750    _env_int_range
 18287-18300  _event_webhook
 13149-13162  _evolution_loop
  6026-6060   _extract_file_payload
  2375-2377   _extract_urls_from_streamurl_node
 21562-21569  _f2b_sudo_hint
  1467-1478   _fanout_ziele
 26483-26546  _fatal_vom_botteil
 25265-25280  _fd_grenze_anheben
  4801-4811   _fehler_text
 10925-10943  _fetch_proxy_list
 18841-18869  _fetch_tiktok_room_id
   826-829    _ff_cmd
 19243-19256  _ffprobe_masse
 13987-13992  _find_chromium
  3558-3560   _find_external_recorder
  2380-2382   _find_stream_urls
 12853-12878  _fire_webhooks
  7862-7871   _fork_safe
   933-946    _freeai_chat_sync_metered
 21608-21612  _geo_lookup_ips
  3830-3839   _get_ai_session
  7695-7735   _get_live_info
  3018-3025   _get_resolve_semaphore
  8328-8724   _handle_single_tracking
 25465-25467  _hb
 25470-25487  _hb_while
 13437-13439  _highlight_cfg
 13442-13471  _highlight_observe
 14038-14046  _htmlov_bild_schreiben
 14016-14035  _htmlov_dauerbrowser
 13995-14013  _htmlov_screenshot_cmd
 18546-18556  _httpx_proxy
 12886-12898  _in_quiet_hours
 26311-26322  _init_db_oder_abbruch
 27130-27161  _install_fast_eventloop
 10117-10171  _install_fast_json
 12480-12496  _install_faulthandler
 20227-20236  _intel_ensure_schema
 20279-20314  _intel_index_loop
 20248-20263  _intel_index_one
 20239-20245  _intel_semantic
  5326-5335   _is_authorized
  8214-8235   _is_dead
  2365-2367   _is_hevc
 21597-21599  _is_private_ip
  1882-1889   _is_process_running
  6614-6621   _is_quiet_hours
  1386-1395   _is_upload_window
  4666-4681   _iso
 10271-10277  _ist_lokal
 10206-10219  _json_error_handler
  6836-6837   _kick_broadcaster_id
  8089-8096   _kick_cluster_gefunden
  8024-8086   _kick_cluster_weiter
  6748-6790   _kick_follower_count
  6732-6735   _kick_slug
 11930-11937  _kick_user_token
  7994-8021   _kick_ws_pause
 26299-26308  _kickmod_boot
  4256-4259   _kind_from_filename
 12915-12917  _latest_popularity
  1819-1828   _laufstand
 25826-25863  _laufstand_loop
 25389-25427  _leistung_erheben
  7569-7596   _link_video_senden
 19885-19934  _live_react_loop
 19552-19874  _live_react_worker
  3408-3520   _live_status_aufloesen
 17688-17699  _live_transcript_push
 19876-19883  _live_users
 18138-18182  _living_title_loop
 22345-22417  _local_backup_scan
 10188-10202  _log_5xx
 25430-25462  _log_schleuse_pruefen
   816-823    _log_sicher
 14632-14644  _looks_like_codec_err
 14627-14629  _looks_like_source_expired
  7912-7942   _loop_fehler
 12500-12509  _loop_heartbeat
 25171-25204  _loop_lag_monitor
 25218-25238  _loop_stockung_melden
 25241-25251  _loop_takt_starten
 12512-12585  _loop_watchdog_thread
 17565-17582  _loyalty_add
 17556-17562  _loyalty_get
 17585-17593  _loyalty_top
  5008-5027   _manual_status
  8237-8238   _mark_dead
 11544-11560  _marketing_loop
 23719-23737  _maybe_handle_command
 25965-25989  _maybe_hype_clip
 22752-22780  _meme_klassifizieren
 19167-19227  _meme_zusammenschnitt
  4159-4164   _migrate_columns
 23998-24009  _mod_is_exempt
 24012-24017  _mod_warn_first
 24020-24023  _mod_warn_text
 13206-13225  _modlog
 13189-13203  _modlog_schreiben
  1082-1084   _multistream_targets
  3195-3231   _nachschlag_ytdlp
  7874-7875   _nc_create_subprocess_exec
  7878-7879   _nc_create_subprocess_shell
 11867-11884  _news_loop
 13248-13250  _normalize_ingest
  2598-2615   _note_check_duration
  9249-9252   _notify_topic_name
  2788-2794   _offline_ergebnis
  3234-3254   _ohne_url_melden
 17714-17722  _oracle_memories
 17988-18022  _oracle_memorize
 17725-17738  _oracle_persona
 17707-17711  _oracle_recent_text
 13626-13627  _ov_atomic_write
 13617-13619  _ov_bar
 16573-16585  _ov_clip_text
 13622-13623  _ov_oneline
 21274-21303  _overlay_push
 13941-13984  _overlay_render_size
 13317-13321  _overlay_session_reset
 21239-21241  _overlay_src_ok
 16657-16667  _own_invites
 13936-13938  _parse_size
 21791-21871  _parse_ssh_attacks
  7245-7278   _pause_resume_cmd
  2124-2168   _persist_refreshed_cookies
  2027-2059   _pick_checked_pull_proxy
 10308-10321  _pin_auth_value
 10368-10369  _pin_clear_fail
 10348-10351  _pin_locked
 10354-10365  _pin_note_fail
 10324-10345  _pin_ok
 21081-21106  _piper_pick_model
 21166-21217  _piper_say
 12815-12850  _post_json_threaded
 13915-13933  _probe_video_size
  1910-1927   _proc_is_recorder
 11237-11265  _proxy_pool_refresh_loop
  1993-2024   _proxy_report_recording
  8822-8860   _pruefstand_melden
 25300-25311  _pruefung_verworfen
 12465-12467  _prune_stall_dumps
 11614-11786  _public_stats
  2190-2196   _pull_proxy_still
 18258-18284  _push_notify
 10537-10539  _pwa_dir
 10994-11009  _quick_validate_proxy
 12881-12883  _quiet_hours_config
 10502-10535  _rate_guard
 17526-17532  _react_warn
  7782-7821   _reap_proc
  9497-9564   _rec_auto_abschalten
  9444-9494   _rec_frueh_getrennt
  9313-9389   _rec_kategorie_melden
  9392-9441   _rec_totstreak_fortschreiben
  2638-2660   _record_check_outcome
   811-813    _redact_stream_urls
 11164-11234  _refresh_proxy_pool
  2415-2506   _resolve_via_html
  2797-2995   _resolve_via_webcast_api_v2
  3058-3143   _resolve_via_ytdlp
 23328-23457  _resolve_youtube_ingest
  2391-2412   _resolver_stumm
 13300-13311  _restream_active_sources
 14314-14438  _restream_avatar_feeder_start
 14441-14450  _restream_avatar_feeder_stop
 19312-19443  _restream_chat_guardian
 13474-13546  _restream_chat_push
 13603-13612  _restream_chat_push_async
 26194-26249  _restream_durchreicher
 14049-14171  _restream_html_overlay_start
 14174-14191  _restream_html_overlay_stop
 13259-13282  _restream_overlay_files
 19938-19970  _restream_platform_state
 20138-20173  _restream_resume_after_restart
 13577-13600  _restream_status_schreiben
 14498-14570  _restream_tts_enqueue_wav
 13877-13909  _restream_tts_feeder
 13874-13875  _restream_tts_fifo_path
 14453-14480  _restream_tts_start
 14482-14496  _restream_tts_stop
 19976-20135  _restream_verify_loop
 22310-22322  _retention_loop
 22304-22307  _retention_scan
  2745-2747   _room_is_abo
  6064-6181   _run_ai_call
 12608-12621  _run_async_from_flask
 21602-21605  _run_priv
 27118-27126  _run_selfcheck_and_exit
 22325-22336  _s3_client
  8264-8315   _safe_send
  4934-4950   _sample_net_throughput
  2690-2720   _schedule_next_check
 22258-22301  _scheduler_loop
  4167-4169   _schema_pk
 12625-12630  _scraper_session
 24026-24065  _screen_full
 11981-12018  _sec_headers
  2370-2372   _select_stream_from_data_section
 26838-27115  _selfcheck
  9261-9295   _send_live_notice
  1409-1413   _should_defer_upload
 22833-22869  _shrink_for_discord
 10542-10554  _sicheres_ziel
 22138-22176  _sicherheits_erinnerung_loop
 25886-25903  _sign_health_check
 25906-25925  _sign_health_loop
  4684-4709   _sitzung_bestimmen
  7891-7902   _spawn
 27549-27579  _spawn_from_flask
 25314-25320  _speicher_maps
 25323-25338  _speicher_pflegen
 18558-18838  _start_chat_listener
 25283-25297  _start_gesperrt
 12588-12605  _start_loop_watchdog
 11813-11862  _stats_loop
 11792-11795  _stats_output_path
 11798-11810  _stats_write
 21118-21132  _stimme_saubern
 21139-21163  _stimme_schon_gesagt
  8803-8819   _storage_cleanup_loop
 25945-25952  _story_for
  3583-3589   _stream_url_expiry
  3591-3596   _stream_url_ttl
 16620-16627  _streamer_persona_get
 22442-22594  _system_backup
 22603-22633  _system_backup_loop
 12425-12443  _task_auf_bot_schleife
 24854-24870  _telegram_befehlsmenue
  7945-7991   _telegram_polling_fehler
  1447-1464   _telegram_ziele
 10946-10985  _test_proxy
 11492-11508  _testpush_resolve_live
 19238-19240  _text_schreiben
  8240-8261   _tg_sprache_setzen
  9183-9236   _tg_topic_umziehen
  9153-9180   _tg_topic_umzug
  9049-9059   _tg_topics_load_into_mem
  9046-9047   _tg_topics_path
  9061-9068   _tg_topics_save
 10280-10290  _token_ok
  9134-9150   _topic_anlegen
  9071-9080   _topic_forget
 12901-12912  _tracking_max_duration
  4464-4478   _tracking_remove_cleanup
  4495-4507   _tracking_resume_cleanup
  1721-1744   _try_attach_file_handler
 21108-21116  _tts_cleanup
 11468-11472  _tunnel_effective
 25695-25715  _tunnel_lage
 25771-25823  _tunnel_wacht_loop
 20607-20660  _twitch_channel_status
 24068-24213  _twitch_chat_loop
 23126-23139  _twitch_clip_versuchen
 23882-23985  _twitch_eventsub_loop
  1432-1445   _upload_queue_add
  1523-1525   _upload_queue_count
  1415-1424   _upload_queue_load
  1405-1407   _upload_queue_path
  1514-1521   _upload_queue_remove
  1426-1430   _upload_queue_save
  9104-9106   _upload_topic_name
  1527-1571   _upload_window_loop
  7755-7762   _uptime_s
 13236-13245  _url_host
  3257-3356   _url_nachschlag
   893-897    _usage_record_claude
 26059-26081  _v37_pause_source
 26023-26033  _v37_restream_restart
 26036-26056  _v37_unpause_source
  8163-8207   _verbindung_verloren
  6793-6824   _viewer_sample_loop
 10372-10375  _wants_html
  7765-7779   _warn_empty_env
 25508-25629  _watchdog_loop
 23603-23611  _wchat_thank_ok
 18326-18356  _whisper_get_model
  7852-7859   _whisper_native_section
 17513-17519  _whisper_pool
 18450-18482  _whisper_segments
 18358-18374  _whisper_stumm
 18377-18447  _whisper_transcribe
 13674-13831  _write_restream_overlay
 13636-13671  _write_restream_overlay_async
 24237-24333  _youtube_api_chat_loop
 20663-20766  _youtube_api_status
 20769-20836  _youtube_channel_status
 24336-24497  _youtube_chat_loop
 23142-23167  _youtube_clip_versuchen
 23463-23476  _youtube_restream_autoconfig
 23479-23503  _youtube_restream_autoconfig_inner
 23570-23598  _youtube_send
 20904-20945  _youtube_set_channel
 23506-23540  _yt_access_token
 23543-23558  _yt_live_chat_id
 23566-23567  _yt_sendrate_cfg
 24216-24231  _yt_timeout
  3042-3043   _ytdlp_detect_available
  3045-3056   _ytdlp_note_result
 12470-12472  _zombie_child_count
 25373-25386  _zustand_kennzahlen
  7631-7655   about
  4375-4379   add_ai_log_entry
  4292-4295   add_archive_entry
  4972-4974   add_archive_rule
  4712-4783   add_recording
  4439-4456   add_tracking
  6184-6217   ai
  3982-4063   ai_chat
  4097-4107   ai_history_append
  4109-4114   ai_history_clear
  4086-4095   ai_history_load
  4071-4084   ai_rate_limit_check
  6246-6254   aireset
 17855-17874  azrael_chat
 24502-24624  brain_cmd
  3599-3604   build_recording_cmd
  4459-4462   bulk_add_trackings
  7047-7106   bulkadd
  8863-9029   check_all_trackings
  4511-4523   claim_live_transition
 16697-17445  class KickModerator
 14647-16460  class RestreamManager
  8099-8160   class _KickClusterSuche
 11351-11393  classify_proxy_anonymity
  6292-6490   cleanup
  5262-5268   cleanup_old_recordings
  4657-4664   clear_recording
 23170-23191  clip_moment
  4924-4927   compute_storage_forecast
  7169-7242   cookies_cmd
  4430-4436   count_trackings_for_chat
  4362-4373   decide_preferred_recorder
  4302-4305   delete_archive_entry
  4976-4978   delete_archive_rule
  5721-5868   diag
 24736-24797  einnahmen_cmd
  4918-4921   find_recordings_by_fingerprint
  4323-4339   finish_recording_attempt
  4483-4485   get_all_active_trackings
  4390-4392   get_all_checks
  4785-4788   get_all_recordings
  4867-4869   get_all_tags_with_counts
  4895-4898   get_annotations_for_recording
  4297-4300   get_archive_entry
  4888-4891   get_bookmarked_recordings
  2230-2235   get_cookie_health
  4855-4861   get_event_log
  4346-4360   get_last_recording_attempt
  3359-3401   get_live_status
  5201-5204   get_manual_recordings
  4903-4906   get_or_compute_inspect_sync
  5303-5306   get_outcome_breakdown
  4874-4877   get_priority_poll_interval
  4341-4344   get_recent_recording_attempts
  4790-4793   get_recording_by_id
  4881-4884   get_recording_note
  3770-3799   get_redis
  4419-4422   get_stats
  5256-5260   get_storage_stats
  4996-4998   get_tiktok_status_distribution
  4525-4534   get_tracking_state
  4480-4481   get_trackings_for_group
  5217-5220   get_trash_recordings
  9628-10096  handle_recording_finished
 24846-24851  hilfe_cmd
  4182-4247   init_db
  4968-4970   list_archive_rules
  5506-5544   live
  8318-8326   live_check_worker
  3854-3893   llm_chat
  3916-3946   llm_chat_sync
  3901-3913   llm_list_models
  4814-4847   log_event
  1844-1877   log_recording_failure
  7392-7441   logs_cmd
 26549-26828  main
  6220-6243   on_ai_media
  7518-7544   on_ai_reply
  7599-7628   on_azrael_mention
  7660-7690   on_callback
  7553-7566   on_link_video
 17880-17985  oracle_handle
  7281-7284   pause_tracking
  5316-5321   profile_keyboard
  5459-5503   quelle
  7343-7389   quota
  8726-8800   reaper_loop
  4992-4994   record_tiktok_status
  6259-6289   recstatus
  3801-3809   redis_get_json
  3812-3818   redis_set_json
 24873-24883  report_cmd
 11396-11398  report_proxy_result
  2509-2551   resolve_tiktok_live_stream
  5212-5215   restore_recording
  7287-7290   resume_tracking
  4981-4986   run_archive_rules
 24886-25151  run_bot
 12322-12416  run_flask
  4956-4959   sample_bandwidth_for_active
  4382-4388   save_tiktok_check
  4649-4655   set_recording_file
  4488-4492   set_tracking_paused
  5207-5210   soft_delete_recording
 24831-24843  spenden_cmd
  9301-9311   split_and_send_video
  5369-5411   start
  4307-4321   start_recording_attempt
  6493-6531   stats
  5146-5199   stop_manual_recording
  7293-7340   stoprec
  6717-6725   summary_cmd
  7444-7515   sysres
  5870-6014   teststream
  5413-5454   tiktok
  7109-7166   topusers
  5581-5638   track
  5546-5578   track_exact
  5652-5719   tracklist
  5030-5144   trigger_manual_recording
  4610-4647   try_acquire_recording_lock
  5223-5225   universal_search
 24800-24828  unpause_cmd
  5640-5650   untrack
 24627-24733  update_cmd
  4913-4916   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmechat.py        ass, ausschnitt, beenden, beginnen, clip_beginnt, clip_fertig, clip_merken, clips_nehmen, clips_offen, concat_liste, einbrennen_cmd, laeuft, modus, notieren, untertitel_cmd, zusammenschnitt_cmd
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest, stall_grenze
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, luecken, probe_cmd, sekunden, sitzung_id, tonformat, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
beobachtungsdienst.py  fuer_deck, grafana_jetzt, grafana_lage, grafana_unit, grund_text, installiert, prometheus_jetzt, prometheus_lage, selbstheilung_erlaubt, steuern
beobachtungslage.py    grafana, lage, prometheus
betriebslage.py        abschiedswache, bereit, bewerten, haengende_threads, sichern_beim_stopp
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatnachtrag.py        beilage_lesen, beilage_zu, eingearbeitet, ensure_schema, erledigt, fehlversuch, ist_beilage, lesen, offene, stempel, unveraendert, vormerken
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
clientip.py            echte_ip, ist_https, ist_lokal
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, configure, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, gesundheit, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, gesetzte, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbgesundheit.py        messen
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, set_pool
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
discordziele.py        clip_kanal, clip_kanal_des_bereichs, clip_kanal_holen, eigene_kanaele, loeschbar, umzugsmarke, umzugsmarke_lesen
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
durchreicher.py        adresse, ist, main, nutzer_aus, werkzeug, werkzeuge, zieher_cmd, zieher_umgebung, zubringer_cmd
einstellungen.py       class Abgelehnt, db_werte, geheim, gueltiger_name, in_umgebung_laden, katalog, pruefen, schutzgrund, setzen, startbericht, uebernehmen, uebersicht, zuruecksetzen
envdatei.py            class EnvdateiFehler, lesen, main, setzen, wert_lesen, wert_schreiben
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      anzeige_groesse, avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
gegendruck.py          abgewiesen, deckel_auto, fd_grenze_anheben, fd_lage, freigeben, lage, reservieren, reserviert, start_entscheiden, verworfen, zuruecksetzen
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
geschuetzt.py          lage, ruhend, vermerken, verschlossen, zuruecksetzen
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          einwertig, prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, naechster_cluster, naechster_key, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
kickzentrifugo.py      als_frame, antwort_fehler, class KickZentrifugoFehler, connect_cmd, fehler_code, ist_ping, kanal, lage, neue_client_id, neues_token, pause, refresh_cmd, subscribe_cmd, token_aus, ttl_aus, verbindung_body, ws_url_aus, zerlegen, zugang
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              backend, lokal_stand, lokal_zuerst, normal, provider
lagebild.py            bauen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
linkvideo.py           abklingzeit_s, an, aufraeumen, ausgabe_lesen, befehl, bildunterschrift, configure, darf, grund, holen, ist_tiktok, links, max_dauer_s, sperre, werkzeug
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           beste_url, braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, einreihen, entkoppeln, nachziehen, schwaerzen, stoppen, synchrone_handler, verloren, wartend, zuruecksetzen
looplag.py             bremser, erfassen, lage, spaeher_starten, stelle_aus_rahmen, takt, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
mariadbumzug.py        class UmzugAbgebrochen, env_setzen, geoeffnet_von, in_benutzung, quelle_zaehlen, umziehen, vergleichen, ziel_zaehlen
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
meldetakt.py           erfolg, gestoert, melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
overlaybrowser.py      browser_cmd, class Dauerbrowser, class OverlayBrowserFehler
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
profildetail.py        datum, felder, kennzahlen, kontotyp, verlauf
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
prueflage.py           fuer_healthz, lage, merken, uebersicht, vergessen
qrsvg.py               qr_svg
quellprobe.py          empfehlung, form, kurz, main, maske, messen, probe_durchreicher, probe_ffprobe, probe_html, probe_ytdlp, ttl
quellstat.py           lage, zaehlen, zuruecksetzen
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, ein_start_je_ziel, fenstergroesse, freigeben, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, startend, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, bruecke, bruecke_luecke, bruecke_offline, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, fueller, quell_eingang, schriftart, zubringer
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              anlegen, create_schema, index_sicher, kollation_angleichen, modultabellen, parameter, spalten_nachziehen
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendebruecke.py        class Bruecke, class TsUmschreiber, ist_keyframe, pat_pmt_pid, pes_zeit, pid, pmt_stroeme, pmt_urteil, video_pid, weiche_grund
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
sicherungspruefung.py  archiv_lesbar, dump_vollstaendig, pruefen
speicherpflege.py      abgelaufene_weg, alte_stempel_weg, groessen
spendeninfo.py         krypto, paypal, paypal_url, stand, text
spendenziel.py         eingang, fenster_start, ist_monatlich, stand, summe, zeitraum, ziel_eur
sqldialekt.py          bei_konflikt
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
telegramfehler.py      dashboard_umzug, dauer_text, ersatz, grund, ist_fehler, ist_telegram_chat, nur_telegram, standardgruppe, text, zuruecksetzen
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tgmarkdown.py          html_zu_md, teilen
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, garantie, garantie_cmd, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
topicumzug.py          alte_themen, angekommen, erledigt, gesendet, lade, offen, schluessel, speichere
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             ausfuehrbar_im_archiv, build_plan, check, class Plan, class UpdaterConfig, commit_zip_url, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, rechte_angleichen, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlpurl.py            nur_frische, urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DatabaseAgent, class DiskAgent, class GrafanaAgent, class HealthAgent, class LearningAgent, class PrometheusAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
