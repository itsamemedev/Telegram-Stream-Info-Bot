# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 10635  GET              /                                                dashboard
 12690  GET              /api/abo/status                                  api_abo_status
 12644  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11423  GET              /api/automation/status                           api_automation_status
 11445  POST             /api/automation/toggle                           api_automation_toggle
 20810  GET              /api/channel/categories                          api_channel_categories
 20816  POST             /api/channel/set                                 api_channel_set
 20663  GET              /api/channels/status                             api_channels_status
 20337  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20320  GET              /api/clips                                       api_clips
 20366  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20238  GET              /api/debug/threads                               api_debug_threads
 12655  GET              /api/events                                      api_events
 12134  GET              /api/events/stream                               api_events_stream
 11961  GET              /api/health                                      api_health
 20279  POST             /api/highlights/config                           api_highlights_config
 10565  POST             /api/login                                       dashboard_login_submit
 12980  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12049  GET              /api/notify/status                               api_notify_status
 12060  POST             /api/notify/test                                 api_notify_test
 12744  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12721  GET              /api/proxy/trend                                 api_proxy_trend
 20386  GET              /api/tts/<fn>                                    api_tts_file
 21163  GET              /api/upload_window                               api_upload_window
 12251  GET              /archive/<int:eid>/download                      archive_download
 12279  GET              /download/<int:recording_id>                     download
 12208  GET              /health                                          health
 20147  GET              /healthz                                         healthz
 10556  GET              /login                                           dashboard_login_page
 10590  GET              /logout                                          dashboard_logout
 10597  GET              /manifest.webmanifest                            pwa_manifest
 21136  GET              /overlay                                         overlay_page
 10621  GET              /pwa-icon-<variant>.png                          pwa_icon
 10607  GET              /sw.js                                           pwa_service_worker
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
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
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

## Discord-Slash-Commands in discordbot.py (66)

```
  2244  /about                  Ueber diesen Bot
   960  /ai                     
  2244  /aireset                KI-Kontext zuruecksetzen
  1374  /ask                    
  1061  /assign_role            
  1111  /ban                    
  2199  /botstats               
  2244  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2244  /bulkadd                Mehrere User auf einmal tracken · a b c
  2244  /cleanup                Alte Aufnahmen aufraeumen
  1630  /clearwarns             
  2163  /clip                   
  2148  /clipoftheweek          
  1500  /clips                  
  2244  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1016  /create_category        
   987  /create_channel         
  1051  /create_group           
  1026  /create_role            
  1002  /create_voice           
  1252  /daily                  
  2244  /diag                   Vollstaendige Diagnose
  2244  /einnahmen              Einnahmen und Spenden
  1403  /event                  
  1445  /events                 
  1540  /follow                 
  1529  /help                   
  1101  /kick                   
  1227  /leaderboard            
  2244  /live                   Live-Status sofort pruefen · @user
  1487  /livenow                
  2244  /logs                   Letzte Fehler aus dem Log
  2244  /pause                  Tracking pausieren · @user
  1515  /post_test              
  1335  /profile                
  1133  /purge                  
  2244  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2244  /quota                  Speicher-Quota
  1214  /rank                   
  1475  /recstatus              
  1071  /remove_role            
  2244  /report                 Azrael-Sentinel-Wochenreport
   973  /restream_status        
  2244  /resume                 Tracking fortsetzen · @user
  1081  /set_channel_perms      
  1176  /setup_community        
  1193  /setup_targets          
  1572  /stats                  
   932  /status                 
  2244  /stoprec                Laufende Aufnahme sauber beenden · @user
  1668  /streaminfo             
  2244  /summary                Tageszusammenfassung
  2244  /sysres                 System-Ressourcen
  2244  /teststream             Recorder-Selbsttest · @user
  2244  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1121  /timeout                
  1640  /topstreamers           
  2244  /topusers               Top-Streamer nach Aufnahmen
   862  /track                  
  2244  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   945  /tracklist              
  1554  /unfollow               
  2244  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   894  /untrack                
  1593  /warn                   
  1616  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2407  on_member_join
  2364  on_message
  2265  on_raw_reaction_add
  2442  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-490    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (53 Funktionen)

```
  1745-1796   _award_xp
   534-561    _bereich_umziehen
   481-491    _clip_kopieren
  1967-1996   _clip_week_leader
  2020-2034   _clipoftheweek_loop
  2559-2621   _community_events_loop
  1702-1724   _dc_client
  1727-1736   _dc_offen
  2661-2696   _disc_automod_check
   407-412    _disc_sprache_setzen
  1799-1847   _discord_ai_automod
   683-722    _discord_automod
  1850-1870   _discord_azrael_reply
  2037-2518   _discord_run_once
   242-300    _discord_start
   303-357    _ensure_discord_invite
  2524-2556   _ensure_error_channel
   428-441    _ensure_rank_roles
   825-839    _ensure_team_roles
  2624-2654   _error_channel_loop
   732-736    _guard
   652-680    _handle_voice_ai
   415-425    _is_admin
   506-531    _link_video
  1915-1926   _liveboard_loop
   739-757    _on_level_up
   648-649    _par_chat_id
  1999-2017   _post_clip_of_week
  1929-1947   _post_weekly_digest
   444-470    _provision_base_channels
  1467-1561   _reg_betrieb
  1147-1241   _reg_community_setup
  1244-1324   _reg_daily_profil
  1367-1464   _reg_frage_events
   919-975    _reg_info
  1093-1144   _reg_moderation
  1327-1364   _reg_profil
  1042-1090   _reg_rollen
   978-1039   _reg_server
  1564-1651   _reg_streamer
  1654-1699   _reg_system
   853-916    _reg_tracking
   792-822    _run_tg_handler
   635-645    _tracked_usernames
   159-221    _uebernehmen
   494-503    _umzugsmarken
  1879-1912   _update_liveboard
  1950-1964   _weekly_digest_loop
   473-478    _ziel_guild
   564-606    _ziele_abgleichen
   615-632    _ziele_sync_loop
   609-612    _ziele_takt_min
   224-227    starte
```

## Top-Level-Symbole in bot.py (575 Funktionen, 3 Klassen)

```
 26136-26158  _abbruch_datenbank_unlesbar
  2740-2741   _abo_key
  2761-2779   _abo_probe_dump
 26254-26270  _abschied_wachen
 26273-26291  _abschluss
 16602-16609  _ad_allowlist
 17604-17610  _agent_for
 17613-17629  _ai_telemetry
 18126-18144  _alert
 22031-22081  _alert_monitor_loop
 18805-18862  _alte_beilagen_einsammeln
 22463-22525  _announce_loop
  3636-3646   _anthropic_key
  3653-3655   _anthropic_model
 10220-10223  _arg_int
  2732-2737   _as_dict
 25822-25831  _async_exc_handler
 18307-18329  _audio_tap_cmd
 19313-19372  _audio_tap_melden
 18343-18367  _audio_tap_sammler
  9565-9602   _aufnahme_beim_stopp_sichern
 18747-18768  _aufnahme_chat_ausklang
 18731-18744  _aufnahme_chat_beginnen
 18890-18911  _aufnahme_chat_dienst
 19082-19132  _aufnahme_chat_einarbeiten
 18726-18728  _aufnahme_chat_modus
 18914-18963  _aufnahme_chat_nachtrag
 18771-18802  _aufnahme_chat_vormerken
 18881-18887  _aufnahme_chat_wecken
 25071-25073  _aufnahme_deckel
 18966-18987  _aufnahme_fertigmachen
  9605-9623   _aufnahme_platz_frei
 26218-26238  _aufnahmen_abschliessen
 26161-26215  _aufraeumen
 10419-10488  _auth_cookie
 10377-10415  _auth_guard
  1981-1986   _auto_on
 19999-20017  _auto_restream_loop
 14224-14266  _avatar_frames_laden
 23598-23613  _azrael_broadcast_reply
 23498-23520  _azrael_chat_reply
 23470-23495  _azrael_chat_should_reply
 23526-23528  _azrael_gate_cfg
 17634-17648  _azrael_live_state
 21049-21063  _azrael_overlay_state
 18008-18062  _azrael_proactive_loop
 17452-17508  _azrael_reaction_to_chats
 23531-23538  _azrael_reply_all_chats
 23457-23467  _azrael_self_names
 23566-23595  _azrael_send_to
 14185-14221  _azrael_spricht
 14528-14541  _azrael_stimme_stumm
 17654-17675  _azrael_system
 22165-22168  _backup_active
 22246-22259  _backup_loop
 25160-25164  _betrieb
 25895-25904  _brain_crowdsec_snap
 26063-26066  _brain_db_health
 21952-21961  _brain_growth_loop
 10814-10841  _brain_growth_snapshot
  2665-2685   _brain_hint_delay
 25967-26002  _brain_moderation_snap
  6582-6610   _brain_notify
 26069-26091  _brain_recording_snap
 25907-25964  _brain_restream_health
 26094-26107  _brain_tiktok_status_snap
 12113-12130  _browser_push
  6622-6709   _build_daily_summary
 14575-14579  _build_restream_cmd
  5335-5362   _can_stop_tracking
  2094-2116   _capture_set_cookies
 12798-12801  _cfg_get
 12804-12806  _cfg_set
 20771-20806  _channel_set_all
 13381-13384  _chat_connected
 13387-13403  _chat_disconnected
 18875-18878  _chat_einarbeiten_async
  9080-9091   _chat_is_forum
 18695-18720  _chat_listener_abbauen
 13423-13425  _chat_sanitize
 13366-13378  _chat_stat
 13406-13409  _chat_stats_snapshot
  3954-3966   _check_ai_models_sync
 11096-11139  _classify_pool_anonymity
 11142-11159  _classify_pool_anonymity_bg
   902-924    _claude_chat_sync_metered
 10252-10258  _client_ip
 23097-23111  _clip_chat_ass
 22609-22643  _clip_prune
 22646-22656  _clip_recfile_for
 23020-23085  _clip_schneiden
 23114-23120  _clip_should_velocity
 22698-22783  _clip_to_discord
 19053-19058  _clips_abwarten
  3840-3849   _close_ai_session
 23644-23659  _cohost_broadcast
 23629-23630  _cohost_cfg
 23685-23697  _cohost_fire_highlight
 23633-23641  _cohost_gate
 23662-23682  _cohost_highlight
 10744-10746  _conv_messages
  6981-7042   _cookie_alarm_loop
  2184-2185   _cookie_autofetch_info
  2168-2172   _cookie_autorefresh_info
 25529-25551  _cookie_bezug_loop
 25554-25579  _cookie_bezug_runde
  2071-2075   _cookie_header
 10261-10266  _cookie_sicher
  2197-2211   _cookies_selbst_holen
  4170-4172   _create_index_safe
 21495-21609  _crowdsec_status
 21441-21492  _crowdsec_via_lapi
 21345-21363  _cscli_bin
 21372-21385  _cscli_path
  6871-6896   _daily_summary_loop
 21403-21420  _darf_journal_lesen
  3165-3190   _darf_ytdlp_nachschlagen
 12294-12315  _dashboard_adresse
  1479-1509   _dashboard_trackings_umziehen
 23088-23094  _datei_weg
 22005-22028  _db_maintenance_loop
  6840-6868   _db_vacuum_loop
 16625-16649  _detect_foreign_ad
  1661-1672   _diag_path_owner
 17913-17958  _director_finalize
 19302-19309  _director_for
 17862-17910  _director_mark
 22933-22936  _disc_state_get
 22939-22946  _disc_state_set
 21933-21942  _discord_bot_starten
 21896-21907  _discord_einladung_merken
 21945-21949  _discord_invite
 21910-21930  _discord_kontext
 22894-22930  _discord_live_thread
 18065-18077  _discord_notify
 21868-21893  _discord_ops_alert
 22794-22890  _discord_post_user
 22528-22534  _discord_stop
  6899-6976   _disk_alarm_loop
 25454-25503  _disk_autoclean
 25677-25690  _disk_guard_loop
 14163-14170  _drossel_hoeher
 14159-14160  _drossel_stufe
 14173-14181  _drossel_zuruecksetzen
 12471-12473  _dump_all_threads
 25167-25181  _einstellungen_startzeile
 11022-11085  _enrich_proxies_with_geo
  2240-2301   _ensure_cookie_file_netscape
  9253-9256   _ensure_notify_topic
 11266-11303  _ensure_proxy_ready
  9107-9129   _ensure_topic
   744-746    _env_int
   749-751    _env_int_range
 18110-18123  _event_webhook
 13149-13162  _evolution_loop
  6024-6058   _extract_file_payload
  2373-2375   _extract_urls_from_streamurl_node
 21388-21395  _f2b_sudo_hint
  1465-1476   _fanout_ziele
 26294-26357  _fatal_vom_botteil
 25076-25091  _fd_grenze_anheben
  4799-4809   _fehler_text
 10923-10941  _fetch_proxy_list
 18664-18692  _fetch_tiktok_room_id
   827-830    _ff_cmd
 19066-19079  _ffprobe_masse
 13992-13997  _find_chromium
  3556-3558   _find_external_recorder
  2378-2380   _find_stream_urls
 12849-12874  _fire_webhooks
  7860-7869   _fork_safe
   935-948    _freeai_chat_sync_metered
 21434-21438  _geo_lookup_ips
  3828-3837   _get_ai_session
  7693-7733   _get_live_info
  3016-3023   _get_resolve_semaphore
  8326-8722   _handle_single_tracking
 25276-25278  _hb
 25281-25298  _hb_while
 13437-13439  _highlight_cfg
 13442-13471  _highlight_observe
 14000-14018  _htmlov_screenshot_cmd
 18369-18379  _httpx_proxy
 12882-12894  _in_quiet_hours
 26122-26133  _init_db_oder_abbruch
 26941-26972  _install_fast_eventloop
 10115-10169  _install_fast_json
 12476-12492  _install_faulthandler
 20050-20059  _intel_ensure_schema
 20102-20137  _intel_index_loop
 20071-20086  _intel_index_one
 20062-20068  _intel_semantic
  5324-5333   _is_authorized
  8212-8233   _is_dead
  2363-2365   _is_hevc
 21423-21425  _is_private_ip
  1880-1887   _is_process_running
  6612-6619   _is_quiet_hours
  1384-1393   _is_upload_window
  4664-4679   _iso
 10269-10275  _ist_lokal
 10204-10217  _json_error_handler
  6834-6835   _kick_broadcaster_id
  8087-8094   _kick_cluster_gefunden
  8022-8084   _kick_cluster_weiter
  6746-6788   _kick_follower_count
  6730-6733   _kick_slug
 11926-11933  _kick_user_token
  7992-8019   _kick_ws_pause
 26110-26119  _kickmod_boot
  4254-4257   _kind_from_filename
 12911-12913  _latest_popularity
  1817-1826   _laufstand
 25637-25674  _laufstand_loop
 25200-25238  _leistung_erheben
  7567-7594   _link_video_senden
 19708-19757  _live_react_loop
 19375-19697  _live_react_worker
  3406-3518   _live_status_aufloesen
 17511-17522  _live_transcript_push
 19699-19706  _live_users
 17961-18005  _living_title_loop
 22171-22243  _local_backup_scan
 10186-10200  _log_5xx
 25241-25273  _log_schleuse_pruefen
   817-824    _log_sicher
 14587-14599  _looks_like_codec_err
 14582-14584  _looks_like_source_expired
  7910-7940   _loop_fehler
 12496-12505  _loop_heartbeat
 24982-25015  _loop_lag_monitor
 25029-25049  _loop_stockung_melden
 25052-25062  _loop_takt_starten
 12508-12581  _loop_watchdog_thread
 17388-17405  _loyalty_add
 17379-17385  _loyalty_get
 17408-17416  _loyalty_top
 13021-13023  _manual_donations_total
  5006-5025   _manual_status
  8235-8236   _mark_dead
 11542-11558  _marketing_loop
 23545-23563  _maybe_handle_command
 25776-25800  _maybe_hype_clip
 22578-22606  _meme_klassifizieren
 18990-19050  _meme_zusammenschnitt
  4157-4162   _migrate_columns
 23824-23835  _mod_is_exempt
 23838-23843  _mod_warn_first
 23846-23849  _mod_warn_text
 13206-13225  _modlog
 13189-13203  _modlog_schreiben
  1080-1082   _multistream_targets
  3193-3229   _nachschlag_ytdlp
  7872-7873   _nc_create_subprocess_exec
  7876-7877   _nc_create_subprocess_shell
 11863-11880  _news_loop
 13248-13250  _normalize_ingest
  2596-2613   _note_check_duration
  9247-9250   _notify_topic_name
  2786-2792   _offline_ergebnis
  3232-3252   _ohne_url_melden
 17537-17545  _oracle_memories
 17811-17845  _oracle_memorize
 17548-17561  _oracle_persona
 17530-17534  _oracle_recent_text
 13626-13627  _ov_atomic_write
 13617-13619  _ov_bar
 16528-16540  _ov_clip_text
 13622-13623  _ov_oneline
 21100-21129  _overlay_push
 13946-13989  _overlay_render_size
 13317-13321  _overlay_session_reset
 21065-21067  _overlay_src_ok
 16612-16622  _own_invites
 13941-13943  _parse_size
 21617-21697  _parse_ssh_attacks
  7243-7276   _pause_resume_cmd
  2122-2166   _persist_refreshed_cookies
  2025-2057   _pick_checked_pull_proxy
 10306-10319  _pin_auth_value
 10366-10367  _pin_clear_fail
 10346-10349  _pin_locked
 10352-10363  _pin_note_fail
 10322-10343  _pin_ok
 20907-20932  _piper_pick_model
 20992-21043  _piper_say
 12811-12846  _post_json_threaded
 13920-13938  _probe_video_size
  1908-1925   _proc_is_recorder
 11235-11263  _proxy_pool_refresh_loop
  1991-2022   _proxy_report_recording
  8820-8858   _pruefstand_melden
 25111-25122  _pruefung_verworfen
 12461-12463  _prune_stall_dumps
 11612-11782  _public_stats
  2188-2194   _pull_proxy_still
 18081-18107  _push_notify
 10535-10537  _pwa_dir
 10992-11007  _quick_validate_proxy
 12877-12879  _quiet_hours_config
 10500-10533  _rate_guard
 17349-17355  _react_warn
  7780-7819   _reap_proc
  9495-9562   _rec_auto_abschalten
  9442-9492   _rec_frueh_getrennt
  9311-9387   _rec_kategorie_melden
  9390-9439   _rec_totstreak_fortschreiben
  2636-2658   _record_check_outcome
   812-814    _redact_stream_urls
 11162-11232  _refresh_proxy_pool
  2413-2504   _resolve_via_html
  2795-2993   _resolve_via_webcast_api_v2
  3056-3141   _resolve_via_ytdlp
 23154-23283  _resolve_youtube_ingest
  2389-2410   _resolver_stumm
 13300-13311  _restream_active_sources
 14269-14393  _restream_avatar_feeder_start
 14396-14405  _restream_avatar_feeder_stop
 19135-19266  _restream_chat_guardian
 13474-13546  _restream_chat_push
 13603-13612  _restream_chat_push_async
 26005-26060  _restream_durchreicher
 14021-14130  _restream_html_overlay_start
 14133-14146  _restream_html_overlay_stop
 13259-13282  _restream_overlay_files
 19761-19793  _restream_platform_state
 19961-19996  _restream_resume_after_restart
 13577-13600  _restream_status_schreiben
 14453-14525  _restream_tts_enqueue_wav
 13882-13914  _restream_tts_feeder
 13879-13880  _restream_tts_fifo_path
 14408-14435  _restream_tts_start
 14437-14451  _restream_tts_stop
 19799-19958  _restream_verify_loop
 22136-22148  _retention_loop
 22130-22133  _retention_scan
  2743-2745   _room_is_abo
  6062-6179   _run_ai_call
 12604-12617  _run_async_from_flask
 21428-21431  _run_priv
 26929-26937  _run_selfcheck_and_exit
 22151-22162  _s3_client
  8262-8313   _safe_send
  4932-4948   _sample_net_throughput
  2688-2718   _schedule_next_check
 22084-22127  _scheduler_loop
  4165-4167   _schema_pk
 12621-12626  _scraper_session
 23852-23891  _screen_full
 11977-12014  _sec_headers
  2368-2370   _select_stream_from_data_section
 26649-26926  _selfcheck
  9259-9293   _send_live_notice
  1407-1411   _should_defer_upload
 22659-22695  _shrink_for_discord
 10540-10552  _sicheres_ziel
 21964-22002  _sicherheits_erinnerung_loop
 25697-25714  _sign_health_check
 25717-25736  _sign_health_loop
  4682-4707   _sitzung_bestimmen
  7889-7900   _spawn
 27360-27390  _spawn_from_flask
 25125-25131  _speicher_maps
 25134-25149  _speicher_pflegen
 18381-18661  _start_chat_listener
 25094-25108  _start_gesperrt
 12584-12601  _start_loop_watchdog
 11809-11858  _stats_loop
 11788-11791  _stats_output_path
 11794-11806  _stats_write
 20944-20958  _stimme_saubern
 20965-20989  _stimme_schon_gesagt
  8801-8817   _storage_cleanup_loop
 25756-25763  _story_for
  3581-3587   _stream_url_expiry
  3589-3594   _stream_url_ttl
 16575-16582  _streamer_persona_get
 22268-22420  _system_backup
 22429-22459  _system_backup_loop
 12421-12439  _task_auf_bot_schleife
 24665-24681  _telegram_befehlsmenue
  7943-7989   _telegram_polling_fehler
  1445-1462   _telegram_ziele
 10944-10983  _test_proxy
 11490-11506  _testpush_resolve_live
 19061-19063  _text_schreiben
  8238-8259   _tg_sprache_setzen
  9181-9234   _tg_topic_umziehen
  9151-9178   _tg_topic_umzug
  9047-9057   _tg_topics_load_into_mem
  9044-9045   _tg_topics_path
  9059-9066   _tg_topics_save
 10278-10288  _token_ok
  9132-9148   _topic_anlegen
  9069-9078   _topic_forget
 12897-12908  _tracking_max_duration
  4462-4476   _tracking_remove_cleanup
  4493-4505   _tracking_resume_cleanup
  1719-1742   _try_attach_file_handler
 20934-20942  _tts_cleanup
 11466-11470  _tunnel_effective
 25506-25526  _tunnel_lage
 25582-25634  _tunnel_wacht_loop
 20430-20483  _twitch_channel_status
 23894-24039  _twitch_chat_loop
 22952-22965  _twitch_clip_versuchen
 23708-23811  _twitch_eventsub_loop
  1430-1443   _upload_queue_add
  1521-1523   _upload_queue_count
  1413-1422   _upload_queue_load
  1403-1405   _upload_queue_path
  1512-1519   _upload_queue_remove
  1424-1428   _upload_queue_save
  9102-9104   _upload_topic_name
  1525-1569   _upload_window_loop
  7753-7760   _uptime_s
 13236-13245  _url_host
  3255-3354   _url_nachschlag
   895-899    _usage_record_claude
 25870-25892  _v37_pause_source
 25834-25844  _v37_restream_restart
 25847-25867  _v37_unpause_source
  8161-8205   _verbindung_verloren
  6791-6822   _viewer_sample_loop
 10370-10373  _wants_html
  7763-7777   _warn_empty_env
 25319-25440  _watchdog_loop
 23429-23437  _wchat_thank_ok
 18149-18179  _whisper_get_model
  7850-7857   _whisper_native_section
 17336-17342  _whisper_pool
 18273-18305  _whisper_segments
 18181-18197  _whisper_stumm
 18200-18270  _whisper_transcribe
 13674-13836  _write_restream_overlay
 13636-13671  _write_restream_overlay_async
 24063-24159  _youtube_api_chat_loop
 20486-20589  _youtube_api_status
 20592-20659  _youtube_channel_status
 24162-24323  _youtube_chat_loop
 22968-22993  _youtube_clip_versuchen
 23289-23302  _youtube_restream_autoconfig
 23305-23329  _youtube_restream_autoconfig_inner
 23396-23424  _youtube_send
 20727-20768  _youtube_set_channel
 23332-23366  _yt_access_token
 23369-23384  _yt_live_chat_id
 23392-23393  _yt_sendrate_cfg
 24042-24057  _yt_timeout
  3040-3041   _ytdlp_detect_available
  3043-3054   _ytdlp_note_result
 12466-12468  _zombie_child_count
 25184-25197  _zustand_kennzahlen
  7629-7653   about
  4373-4377   add_ai_log_entry
  4290-4293   add_archive_entry
  4970-4972   add_archive_rule
  4710-4781   add_recording
  4437-4454   add_tracking
  6182-6215   ai
  3980-4061   ai_chat
  4095-4105   ai_history_append
  4107-4112   ai_history_clear
  4084-4093   ai_history_load
  4069-4082   ai_rate_limit_check
  6244-6252   aireset
 17678-17697  azrael_chat
 24328-24450  brain_cmd
  3597-3602   build_recording_cmd
  4457-4460   bulk_add_trackings
  7045-7104   bulkadd
  8861-9027   check_all_trackings
  4509-4521   claim_live_transition
 16652-17268  class KickModerator
 14602-16415  class RestreamManager
  8097-8158   class _KickClusterSuche
 11349-11391  classify_proxy_anonymity
  6290-6488   cleanup
  5260-5266   cleanup_old_recordings
  4655-4662   clear_recording
 22996-23017  clip_moment
  4922-4925   compute_storage_forecast
  7167-7240   cookies_cmd
  4428-4434   count_trackings_for_chat
  4360-4371   decide_preferred_recorder
  4300-4303   delete_archive_entry
  4974-4976   delete_archive_rule
  5719-5866   diag
 24562-24623  einnahmen_cmd
  4916-4919   find_recordings_by_fingerprint
  4321-4337   finish_recording_attempt
  4481-4483   get_all_active_trackings
  4388-4390   get_all_checks
  4783-4786   get_all_recordings
  4865-4867   get_all_tags_with_counts
  4893-4896   get_annotations_for_recording
  4295-4298   get_archive_entry
  4886-4889   get_bookmarked_recordings
  2228-2233   get_cookie_health
  4853-4859   get_event_log
  4344-4358   get_last_recording_attempt
  3357-3399   get_live_status
  5199-5202   get_manual_recordings
  4901-4904   get_or_compute_inspect_sync
  5301-5304   get_outcome_breakdown
  4872-4875   get_priority_poll_interval
  4339-4342   get_recent_recording_attempts
  4788-4791   get_recording_by_id
  4879-4882   get_recording_note
  3768-3797   get_redis
  4417-4420   get_stats
  5254-5258   get_storage_stats
  4994-4996   get_tiktok_status_distribution
  4523-4532   get_tracking_state
  4478-4479   get_trackings_for_group
  5215-5218   get_trash_recordings
  9626-10094  handle_recording_finished
 24657-24662  hilfe_cmd
  4180-4245   init_db
  4966-4968   list_archive_rules
  5504-5542   live
  8316-8324   live_check_worker
  3852-3891   llm_chat
  3914-3944   llm_chat_sync
  3899-3911   llm_list_models
  4812-4845   log_event
  1842-1875   log_recording_failure
  7390-7439   logs_cmd
 26360-26639  main
  6218-6241   on_ai_media
  7516-7542   on_ai_reply
  7597-7626   on_azrael_mention
  7658-7688   on_callback
  7551-7564   on_link_video
 17703-17808  oracle_handle
  7279-7282   pause_tracking
  5314-5319   profile_keyboard
  5457-5501   quelle
  7341-7387   quota
  8724-8798   reaper_loop
  4990-4992   record_tiktok_status
  6257-6287   recstatus
  3799-3807   redis_get_json
  3810-3816   redis_set_json
 24684-24694  report_cmd
 11394-11396  report_proxy_result
  2507-2549   resolve_tiktok_live_stream
  5210-5213   restore_recording
  7285-7288   resume_tracking
  4979-4984   run_archive_rules
 24697-24962  run_bot
 12318-12412  run_flask
  4954-4957   sample_bandwidth_for_active
  4380-4386   save_tiktok_check
  4647-4653   set_recording_file
  4486-4490   set_tracking_paused
  5205-5208   soft_delete_recording
  9299-9309   split_and_send_video
  5367-5409   start
  4305-4319   start_recording_attempt
  6491-6529   stats
  5144-5197   stop_manual_recording
  7291-7338   stoprec
  6715-6723   summary_cmd
  7442-7513   sysres
  5868-6012   teststream
  5411-5452   tiktok
  7107-7164   topusers
  5579-5636   track
  5544-5576   track_exact
  5650-5717   tracklist
  5028-5142   trigger_manual_recording
  4608-4645   try_acquire_recording_lock
  5221-5223   universal_search
 24626-24654  unpause_cmd
  5638-5648   untrack
 24453-24559  update_cmd
  4911-4914   update_recording_fingerprint
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
crypto.py              addresses, erwartete_namen, fehlende_namen, snapshot
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
