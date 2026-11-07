# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 10582  GET              /                                                dashboard
 12637  GET              /api/abo/status                                  api_abo_status
 12591  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11370  GET              /api/automation/status                           api_automation_status
 11392  POST             /api/automation/toggle                           api_automation_toggle
 20757  GET              /api/channel/categories                          api_channel_categories
 20763  POST             /api/channel/set                                 api_channel_set
 20610  GET              /api/channels/status                             api_channels_status
 20284  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20267  GET              /api/clips                                       api_clips
 20313  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20185  GET              /api/debug/threads                               api_debug_threads
 12602  GET              /api/events                                      api_events
 12081  GET              /api/events/stream                               api_events_stream
 11908  GET              /api/health                                      api_health
 20226  POST             /api/highlights/config                           api_highlights_config
 10512  POST             /api/login                                       dashboard_login_submit
 12927  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11996  GET              /api/notify/status                               api_notify_status
 12007  POST             /api/notify/test                                 api_notify_test
 12691  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12668  GET              /api/proxy/trend                                 api_proxy_trend
 20333  GET              /api/tts/<fn>                                    api_tts_file
 21110  GET              /api/upload_window                               api_upload_window
 12198  GET              /archive/<int:eid>/download                      archive_download
 12226  GET              /download/<int:recording_id>                     download
 12155  GET              /health                                          health
 20094  GET              /healthz                                         healthz
 10503  GET              /login                                           dashboard_login_page
 10537  GET              /logout                                          dashboard_logout
 10544  GET              /manifest.webmanifest                            pwa_manifest
 21083  GET              /overlay                                         overlay_page
 10568  GET              /pwa-icon-<variant>.png                          pwa_icon
 10554  GET              /sw.js                                           pwa_service_worker
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
  2214  /about                  Ueber diesen Bot
   930  /ai                     
  2214  /aireset                KI-Kontext zuruecksetzen
  1344  /ask                    
  1031  /assign_role            
  1081  /ban                    
  2169  /botstats               
  2214  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2214  /bulkadd                Mehrere User auf einmal tracken · a b c
  2214  /cleanup                Alte Aufnahmen aufraeumen
  1600  /clearwarns             
  2133  /clip                   
  2118  /clipoftheweek          
  1470  /clips                  
  2214  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
   986  /create_category        
   957  /create_channel         
  1021  /create_group           
   996  /create_role            
   972  /create_voice           
  1222  /daily                  
  2214  /diag                   Vollstaendige Diagnose
  2214  /einnahmen              Einnahmen und Spenden
  1373  /event                  
  1415  /events                 
  1510  /follow                 
  1499  /help                   
  1071  /kick                   
  1197  /leaderboard            
  2214  /live                   Live-Status sofort pruefen · @user
  1457  /livenow                
  2214  /logs                   Letzte Fehler aus dem Log
  2214  /pause                  Tracking pausieren · @user
  1485  /post_test              
  1305  /profile                
  1103  /purge                  
  2214  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2214  /quota                  Speicher-Quota
  1184  /rank                   
  1445  /recstatus              
  1041  /remove_role            
  2214  /report                 Azrael-Sentinel-Wochenreport
   943  /restream_status        
  2214  /resume                 Tracking fortsetzen · @user
  1051  /set_channel_perms      
  1146  /setup_community        
  1163  /setup_targets          
  1542  /stats                  
   902  /status                 
  2214  /stoprec                Laufende Aufnahme sauber beenden · @user
  1638  /streaminfo             
  2214  /summary                Tageszusammenfassung
  2214  /sysres                 System-Ressourcen
  2214  /teststream             Recorder-Selbsttest · @user
  2214  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1091  /timeout                
  1610  /topstreamers           
  2214  /topusers               Top-Streamer nach Aufnahmen
   832  /track                  
  2214  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   915  /tracklist              
  1524  /unfollow               
  2214  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   864  /untrack                
  1563  /warn                   
  1586  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2372  on_member_join
  2334  on_message
  2235  on_raw_reaction_add
  2407  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-490    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (52 Funktionen)

```
  1715-1766   _award_xp
   504-531    _bereich_umziehen
   479-489    _clip_kopieren
  1937-1966   _clip_week_leader
  1990-2004   _clipoftheweek_loop
  2524-2586   _community_events_loop
  1672-1694   _dc_client
  1697-1706   _dc_offen
  2626-2661   _disc_automod_check
   405-410    _disc_sprache_setzen
  1769-1817   _discord_ai_automod
   653-692    _discord_automod
  1820-1840   _discord_azrael_reply
  2007-2483   _discord_run_once
   240-298    _discord_start
   301-355    _ensure_discord_invite
  2489-2521   _ensure_error_channel
   426-439    _ensure_rank_roles
   795-809    _ensure_team_roles
  2589-2619   _error_channel_loop
   702-706    _guard
   622-650    _handle_voice_ai
   413-423    _is_admin
  1885-1896   _liveboard_loop
   709-727    _on_level_up
   618-619    _par_chat_id
  1969-1987   _post_clip_of_week
  1899-1917   _post_weekly_digest
   442-468    _provision_base_channels
  1437-1531   _reg_betrieb
  1117-1211   _reg_community_setup
  1214-1294   _reg_daily_profil
  1337-1434   _reg_frage_events
   889-945    _reg_info
  1063-1114   _reg_moderation
  1297-1334   _reg_profil
  1012-1060   _reg_rollen
   948-1009   _reg_server
  1534-1621   _reg_streamer
  1624-1669   _reg_system
   823-886    _reg_tracking
   762-792    _run_tg_handler
   605-615    _tracked_usernames
   157-219    _uebernehmen
   492-501    _umzugsmarken
  1849-1882   _update_liveboard
  1920-1934   _weekly_digest_loop
   471-476    _ziel_guild
   534-576    _ziele_abgleichen
   585-602    _ziele_sync_loop
   579-582    _ziele_takt_min
   222-225    starte
```

## Top-Level-Symbole in bot.py (573 Funktionen, 3 Klassen)

```
 26077-26099  _abbruch_datenbank_unlesbar
  2739-2740   _abo_key
  2760-2778   _abo_probe_dump
 26195-26211  _abschied_wachen
 26214-26232  _abschluss
 16549-16556  _ad_allowlist
 17551-17557  _agent_for
 17560-17576  _ai_telemetry
 18073-18091  _alert
 21978-22028  _alert_monitor_loop
 18752-18809  _alte_beilagen_einsammeln
 22410-22472  _announce_loop
  3635-3645   _anthropic_key
  3652-3654   _anthropic_model
 10167-10170  _arg_int
  2731-2736   _as_dict
 25763-25772  _async_exc_handler
 18254-18276  _audio_tap_cmd
 19260-19319  _audio_tap_melden
 18290-18314  _audio_tap_sammler
  9512-9549   _aufnahme_beim_stopp_sichern
 18694-18715  _aufnahme_chat_ausklang
 18678-18691  _aufnahme_chat_beginnen
 18837-18858  _aufnahme_chat_dienst
 19029-19079  _aufnahme_chat_einarbeiten
 18673-18675  _aufnahme_chat_modus
 18861-18910  _aufnahme_chat_nachtrag
 18718-18749  _aufnahme_chat_vormerken
 18828-18834  _aufnahme_chat_wecken
 25012-25014  _aufnahme_deckel
 18913-18934  _aufnahme_fertigmachen
  9552-9570   _aufnahme_platz_frei
 26159-26179  _aufnahmen_abschliessen
 26102-26156  _aufraeumen
 10366-10435  _auth_cookie
 10324-10362  _auth_guard
  1980-1985   _auto_on
 19946-19964  _auto_restream_loop
 14171-14213  _avatar_frames_laden
 23545-23560  _azrael_broadcast_reply
 23445-23467  _azrael_chat_reply
 23417-23442  _azrael_chat_should_reply
 23473-23475  _azrael_gate_cfg
 17581-17595  _azrael_live_state
 20996-21010  _azrael_overlay_state
 17955-18009  _azrael_proactive_loop
 17399-17455  _azrael_reaction_to_chats
 23478-23485  _azrael_reply_all_chats
 23404-23414  _azrael_self_names
 23513-23542  _azrael_send_to
 14132-14168  _azrael_spricht
 14475-14488  _azrael_stimme_stumm
 17601-17622  _azrael_system
 22112-22115  _backup_active
 22193-22206  _backup_loop
 25101-25105  _betrieb
 25836-25845  _brain_crowdsec_snap
 26004-26007  _brain_db_health
 21899-21908  _brain_growth_loop
 10761-10788  _brain_growth_snapshot
  2664-2684   _brain_hint_delay
 25908-25943  _brain_moderation_snap
  6581-6609   _brain_notify
 26010-26032  _brain_recording_snap
 25848-25905  _brain_restream_health
 26035-26048  _brain_tiktok_status_snap
 12060-12077  _browser_push
  6621-6708   _build_daily_summary
 14522-14526  _build_restream_cmd
  5334-5361   _can_stop_tracking
  2093-2115   _capture_set_cookies
 12745-12748  _cfg_get
 12751-12753  _cfg_set
 20718-20753  _channel_set_all
 13328-13331  _chat_connected
 13334-13350  _chat_disconnected
 18822-18825  _chat_einarbeiten_async
  9027-9038   _chat_is_forum
 18642-18667  _chat_listener_abbauen
 13370-13372  _chat_sanitize
 13313-13325  _chat_stat
 13353-13356  _chat_stats_snapshot
  3953-3965   _check_ai_models_sync
 11043-11086  _classify_pool_anonymity
 11089-11106  _classify_pool_anonymity_bg
   901-923    _claude_chat_sync_metered
 10199-10205  _client_ip
 23044-23058  _clip_chat_ass
 22556-22590  _clip_prune
 22593-22603  _clip_recfile_for
 22967-23032  _clip_schneiden
 23061-23067  _clip_should_velocity
 22645-22730  _clip_to_discord
 19000-19005  _clips_abwarten
  3839-3848   _close_ai_session
 23591-23606  _cohost_broadcast
 23576-23577  _cohost_cfg
 23632-23644  _cohost_fire_highlight
 23580-23588  _cohost_gate
 23609-23629  _cohost_highlight
 10691-10693  _conv_messages
  6980-7041   _cookie_alarm_loop
  2183-2184   _cookie_autofetch_info
  2167-2171   _cookie_autorefresh_info
 25470-25492  _cookie_bezug_loop
 25495-25520  _cookie_bezug_runde
  2070-2074   _cookie_header
 10208-10213  _cookie_sicher
  2196-2210   _cookies_selbst_holen
  4169-4171   _create_index_safe
 21442-21556  _crowdsec_status
 21388-21439  _crowdsec_via_lapi
 21292-21310  _cscli_bin
 21319-21332  _cscli_path
  6870-6895   _daily_summary_loop
 21350-21367  _darf_journal_lesen
  3164-3189   _darf_ytdlp_nachschlagen
 12241-12262  _dashboard_adresse
  1478-1508   _dashboard_trackings_umziehen
 23035-23041  _datei_weg
 21952-21975  _db_maintenance_loop
  6839-6867   _db_vacuum_loop
 16572-16596  _detect_foreign_ad
  1660-1671   _diag_path_owner
 17860-17905  _director_finalize
 19249-19256  _director_for
 17809-17857  _director_mark
 22880-22883  _disc_state_get
 22886-22893  _disc_state_set
 21880-21889  _discord_bot_starten
 21843-21854  _discord_einladung_merken
 21892-21896  _discord_invite
 21857-21877  _discord_kontext
 22841-22877  _discord_live_thread
 18012-18024  _discord_notify
 21815-21840  _discord_ops_alert
 22741-22837  _discord_post_user
 22475-22481  _discord_stop
  6898-6975   _disk_alarm_loop
 25395-25444  _disk_autoclean
 25618-25631  _disk_guard_loop
 14110-14117  _drossel_hoeher
 14106-14107  _drossel_stufe
 14120-14128  _drossel_zuruecksetzen
 12418-12420  _dump_all_threads
 25108-25122  _einstellungen_startzeile
 10969-11032  _enrich_proxies_with_geo
  2239-2300   _ensure_cookie_file_netscape
  9200-9203   _ensure_notify_topic
 11213-11250  _ensure_proxy_ready
  9054-9076   _ensure_topic
   743-745    _env_int
   748-750    _env_int_range
 18057-18070  _event_webhook
 13096-13109  _evolution_loop
  6023-6057   _extract_file_payload
  2372-2374   _extract_urls_from_streamurl_node
 21335-21342  _f2b_sudo_hint
  1464-1475   _fanout_ziele
 26235-26298  _fatal_vom_botteil
 25017-25032  _fd_grenze_anheben
  4798-4808   _fehler_text
 10870-10888  _fetch_proxy_list
 18611-18639  _fetch_tiktok_room_id
   826-829    _ff_cmd
 19013-19026  _ffprobe_masse
 13939-13944  _find_chromium
  3555-3557   _find_external_recorder
  2377-2379   _find_stream_urls
 12796-12821  _fire_webhooks
  7807-7816   _fork_safe
   934-947    _freeai_chat_sync_metered
 21381-21385  _geo_lookup_ips
  3827-3836   _get_ai_session
  7640-7680   _get_live_info
  3015-3022   _get_resolve_semaphore
  8273-8669   _handle_single_tracking
 25217-25219  _hb
 25222-25239  _hb_while
 13384-13386  _highlight_cfg
 13389-13418  _highlight_observe
 13947-13965  _htmlov_screenshot_cmd
 18316-18326  _httpx_proxy
 12829-12841  _in_quiet_hours
 26063-26074  _init_db_oder_abbruch
 26882-26913  _install_fast_eventloop
 10062-10116  _install_fast_json
 12423-12439  _install_faulthandler
 19997-20006  _intel_ensure_schema
 20049-20084  _intel_index_loop
 20018-20033  _intel_index_one
 20009-20015  _intel_semantic
  5323-5332   _is_authorized
  8159-8180   _is_dead
  2362-2364   _is_hevc
 21370-21372  _is_private_ip
  1879-1886   _is_process_running
  6611-6618   _is_quiet_hours
  1383-1392   _is_upload_window
  4663-4678   _iso
 10216-10222  _ist_lokal
 10151-10164  _json_error_handler
  6833-6834   _kick_broadcaster_id
  8034-8041   _kick_cluster_gefunden
  7969-8031   _kick_cluster_weiter
  6745-6787   _kick_follower_count
  6729-6732   _kick_slug
 11873-11880  _kick_user_token
  7939-7966   _kick_ws_pause
 26051-26060  _kickmod_boot
  4253-4256   _kind_from_filename
 12858-12860  _latest_popularity
  1816-1825   _laufstand
 25578-25615  _laufstand_loop
 25141-25179  _leistung_erheben
 19655-19704  _live_react_loop
 19322-19644  _live_react_worker
  3405-3517   _live_status_aufloesen
 17458-17469  _live_transcript_push
 19646-19653  _live_users
 17908-17952  _living_title_loop
 22118-22190  _local_backup_scan
 10133-10147  _log_5xx
 25182-25214  _log_schleuse_pruefen
   816-823    _log_sicher
 14534-14546  _looks_like_codec_err
 14529-14531  _looks_like_source_expired
  7857-7887   _loop_fehler
 12443-12452  _loop_heartbeat
 24923-24956  _loop_lag_monitor
 24970-24990  _loop_stockung_melden
 24993-25003  _loop_takt_starten
 12455-12528  _loop_watchdog_thread
 17335-17352  _loyalty_add
 17326-17332  _loyalty_get
 17355-17363  _loyalty_top
 12968-12970  _manual_donations_total
  5005-5024   _manual_status
  8182-8183   _mark_dead
 11489-11505  _marketing_loop
 23492-23510  _maybe_handle_command
 25717-25741  _maybe_hype_clip
 22525-22553  _meme_klassifizieren
 18937-18997  _meme_zusammenschnitt
  4156-4161   _migrate_columns
 23771-23782  _mod_is_exempt
 23785-23790  _mod_warn_first
 23793-23796  _mod_warn_text
 13153-13172  _modlog
 13136-13150  _modlog_schreiben
  1079-1081   _multistream_targets
  3192-3228   _nachschlag_ytdlp
  7819-7820   _nc_create_subprocess_exec
  7823-7824   _nc_create_subprocess_shell
 11810-11827  _news_loop
 13195-13197  _normalize_ingest
  2595-2612   _note_check_duration
  9194-9197   _notify_topic_name
  2785-2791   _offline_ergebnis
  3231-3251   _ohne_url_melden
 17484-17492  _oracle_memories
 17758-17792  _oracle_memorize
 17495-17508  _oracle_persona
 17477-17481  _oracle_recent_text
 13573-13574  _ov_atomic_write
 13564-13566  _ov_bar
 16475-16487  _ov_clip_text
 13569-13570  _ov_oneline
 21047-21076  _overlay_push
 13893-13936  _overlay_render_size
 13264-13268  _overlay_session_reset
 21012-21014  _overlay_src_ok
 16559-16569  _own_invites
 13888-13890  _parse_size
 21564-21644  _parse_ssh_attacks
  7242-7275   _pause_resume_cmd
  2121-2165   _persist_refreshed_cookies
  2024-2056   _pick_checked_pull_proxy
 10253-10266  _pin_auth_value
 10313-10314  _pin_clear_fail
 10293-10296  _pin_locked
 10299-10310  _pin_note_fail
 10269-10290  _pin_ok
 20854-20879  _piper_pick_model
 20939-20990  _piper_say
 12758-12793  _post_json_threaded
 13867-13885  _probe_video_size
  1907-1924   _proc_is_recorder
 11182-11210  _proxy_pool_refresh_loop
  1990-2021   _proxy_report_recording
  8767-8805   _pruefstand_melden
 25052-25063  _pruefung_verworfen
 12408-12410  _prune_stall_dumps
 11559-11729  _public_stats
  2187-2193   _pull_proxy_still
 18028-18054  _push_notify
 10482-10484  _pwa_dir
 10939-10954  _quick_validate_proxy
 12824-12826  _quiet_hours_config
 10447-10480  _rate_guard
 17296-17302  _react_warn
  7727-7766   _reap_proc
  9442-9509   _rec_auto_abschalten
  9389-9439   _rec_frueh_getrennt
  9258-9334   _rec_kategorie_melden
  9337-9386   _rec_totstreak_fortschreiben
  2635-2657   _record_check_outcome
   811-813    _redact_stream_urls
 11109-11179  _refresh_proxy_pool
  2412-2503   _resolve_via_html
  2794-2992   _resolve_via_webcast_api_v2
  3055-3140   _resolve_via_ytdlp
 23101-23230  _resolve_youtube_ingest
  2388-2409   _resolver_stumm
 13247-13258  _restream_active_sources
 14216-14340  _restream_avatar_feeder_start
 14343-14352  _restream_avatar_feeder_stop
 19082-19213  _restream_chat_guardian
 13421-13493  _restream_chat_push
 13550-13559  _restream_chat_push_async
 25946-26001  _restream_durchreicher
 13968-14077  _restream_html_overlay_start
 14080-14093  _restream_html_overlay_stop
 13206-13229  _restream_overlay_files
 19708-19740  _restream_platform_state
 19908-19943  _restream_resume_after_restart
 13524-13547  _restream_status_schreiben
 14400-14472  _restream_tts_enqueue_wav
 13829-13861  _restream_tts_feeder
 13826-13827  _restream_tts_fifo_path
 14355-14382  _restream_tts_start
 14384-14398  _restream_tts_stop
 19746-19905  _restream_verify_loop
 22083-22095  _retention_loop
 22077-22080  _retention_scan
  2742-2744   _room_is_abo
  6061-6178   _run_ai_call
 12551-12564  _run_async_from_flask
 21375-21378  _run_priv
 26870-26878  _run_selfcheck_and_exit
 22098-22109  _s3_client
  8209-8260   _safe_send
  4931-4947   _sample_net_throughput
  2687-2717   _schedule_next_check
 22031-22074  _scheduler_loop
  4164-4166   _schema_pk
 12568-12573  _scraper_session
 23799-23838  _screen_full
 11924-11961  _sec_headers
  2367-2369   _select_stream_from_data_section
 26590-26867  _selfcheck
  9206-9240   _send_live_notice
  1406-1410   _should_defer_upload
 22606-22642  _shrink_for_discord
 10487-10499  _sicheres_ziel
 21911-21949  _sicherheits_erinnerung_loop
 25638-25655  _sign_health_check
 25658-25677  _sign_health_loop
  4681-4706   _sitzung_bestimmen
  7836-7847   _spawn
 27295-27325  _spawn_from_flask
 25066-25072  _speicher_maps
 25075-25090  _speicher_pflegen
 18328-18608  _start_chat_listener
 25035-25049  _start_gesperrt
 12531-12548  _start_loop_watchdog
 11756-11805  _stats_loop
 11735-11738  _stats_output_path
 11741-11753  _stats_write
 20891-20905  _stimme_saubern
 20912-20936  _stimme_schon_gesagt
  8748-8764   _storage_cleanup_loop
 25697-25704  _story_for
  3580-3586   _stream_url_expiry
  3588-3593   _stream_url_ttl
 16522-16529  _streamer_persona_get
 22215-22367  _system_backup
 22376-22406  _system_backup_loop
 12368-12386  _task_auf_bot_schleife
 24612-24628  _telegram_befehlsmenue
  7890-7936   _telegram_polling_fehler
  1444-1461   _telegram_ziele
 10891-10930  _test_proxy
 11437-11453  _testpush_resolve_live
 19008-19010  _text_schreiben
  8185-8206   _tg_sprache_setzen
  9128-9181   _tg_topic_umziehen
  9098-9125   _tg_topic_umzug
  8994-9004   _tg_topics_load_into_mem
  8991-8992   _tg_topics_path
  9006-9013   _tg_topics_save
 10225-10235  _token_ok
  9079-9095   _topic_anlegen
  9016-9025   _topic_forget
 12844-12855  _tracking_max_duration
  4461-4475   _tracking_remove_cleanup
  4492-4504   _tracking_resume_cleanup
  1718-1741   _try_attach_file_handler
 20881-20889  _tts_cleanup
 11413-11417  _tunnel_effective
 25447-25467  _tunnel_lage
 25523-25575  _tunnel_wacht_loop
 20377-20430  _twitch_channel_status
 23841-23986  _twitch_chat_loop
 22899-22912  _twitch_clip_versuchen
 23655-23758  _twitch_eventsub_loop
  1429-1442   _upload_queue_add
  1520-1522   _upload_queue_count
  1412-1421   _upload_queue_load
  1402-1404   _upload_queue_path
  1511-1518   _upload_queue_remove
  1423-1427   _upload_queue_save
  9049-9051   _upload_topic_name
  1524-1568   _upload_window_loop
  7700-7707   _uptime_s
 13183-13192  _url_host
  3254-3353   _url_nachschlag
   894-898    _usage_record_claude
 25811-25833  _v37_pause_source
 25775-25785  _v37_restream_restart
 25788-25808  _v37_unpause_source
  8108-8152   _verbindung_verloren
  6790-6821   _viewer_sample_loop
 10317-10320  _wants_html
  7710-7724   _warn_empty_env
 25260-25381  _watchdog_loop
 23376-23384  _wchat_thank_ok
 18096-18126  _whisper_get_model
  7797-7804   _whisper_native_section
 17283-17289  _whisper_pool
 18220-18252  _whisper_segments
 18128-18144  _whisper_stumm
 18147-18217  _whisper_transcribe
 13621-13783  _write_restream_overlay
 13583-13618  _write_restream_overlay_async
 24010-24106  _youtube_api_chat_loop
 20433-20536  _youtube_api_status
 20539-20606  _youtube_channel_status
 24109-24270  _youtube_chat_loop
 22915-22940  _youtube_clip_versuchen
 23236-23249  _youtube_restream_autoconfig
 23252-23276  _youtube_restream_autoconfig_inner
 23343-23371  _youtube_send
 20674-20715  _youtube_set_channel
 23279-23313  _yt_access_token
 23316-23331  _yt_live_chat_id
 23339-23340  _yt_sendrate_cfg
 23989-24004  _yt_timeout
  3039-3040   _ytdlp_detect_available
  3042-3053   _ytdlp_note_result
 12413-12415  _zombie_child_count
 25125-25138  _zustand_kennzahlen
  7576-7600   about
  4372-4376   add_ai_log_entry
  4289-4292   add_archive_entry
  4969-4971   add_archive_rule
  4709-4780   add_recording
  4436-4453   add_tracking
  6181-6214   ai
  3979-4060   ai_chat
  4094-4104   ai_history_append
  4106-4111   ai_history_clear
  4083-4092   ai_history_load
  4068-4081   ai_rate_limit_check
  6243-6251   aireset
 17625-17644  azrael_chat
 24275-24397  brain_cmd
  3596-3601   build_recording_cmd
  4456-4459   bulk_add_trackings
  7044-7103   bulkadd
  8808-8974   check_all_trackings
  4508-4520   claim_live_transition
 16599-17215  class KickModerator
 14549-16362  class RestreamManager
  8044-8105   class _KickClusterSuche
 11296-11338  classify_proxy_anonymity
  6289-6487   cleanup
  5259-5265   cleanup_old_recordings
  4654-4661   clear_recording
 22943-22964  clip_moment
  4921-4924   compute_storage_forecast
  7166-7239   cookies_cmd
  4427-4433   count_trackings_for_chat
  4359-4370   decide_preferred_recorder
  4299-4302   delete_archive_entry
  4973-4975   delete_archive_rule
  5718-5865   diag
 24509-24570  einnahmen_cmd
  4915-4918   find_recordings_by_fingerprint
  4320-4336   finish_recording_attempt
  4480-4482   get_all_active_trackings
  4387-4389   get_all_checks
  4782-4785   get_all_recordings
  4864-4866   get_all_tags_with_counts
  4892-4895   get_annotations_for_recording
  4294-4297   get_archive_entry
  4885-4888   get_bookmarked_recordings
  2227-2232   get_cookie_health
  4852-4858   get_event_log
  4343-4357   get_last_recording_attempt
  3356-3398   get_live_status
  5198-5201   get_manual_recordings
  4900-4903   get_or_compute_inspect_sync
  5300-5303   get_outcome_breakdown
  4871-4874   get_priority_poll_interval
  4338-4341   get_recent_recording_attempts
  4787-4790   get_recording_by_id
  4878-4881   get_recording_note
  3767-3796   get_redis
  4416-4419   get_stats
  5253-5257   get_storage_stats
  4993-4995   get_tiktok_status_distribution
  4522-4531   get_tracking_state
  4477-4478   get_trackings_for_group
  5214-5217   get_trash_recordings
  9573-10041  handle_recording_finished
 24604-24609  hilfe_cmd
  4179-4244   init_db
  4965-4967   list_archive_rules
  5503-5541   live
  8263-8271   live_check_worker
  3851-3890   llm_chat
  3913-3943   llm_chat_sync
  3898-3910   llm_list_models
  4811-4844   log_event
  1841-1874   log_recording_failure
  7389-7438   logs_cmd
 26301-26580  main
  6217-6240   on_ai_media
  7515-7541   on_ai_reply
  7544-7573   on_azrael_mention
  7605-7635   on_callback
 17650-17755  oracle_handle
  7278-7281   pause_tracking
  5313-5318   profile_keyboard
  5456-5500   quelle
  7340-7386   quota
  8671-8745   reaper_loop
  4989-4991   record_tiktok_status
  6256-6286   recstatus
  3798-3806   redis_get_json
  3809-3815   redis_set_json
 24631-24641  report_cmd
 11341-11343  report_proxy_result
  2506-2548   resolve_tiktok_live_stream
  5209-5212   restore_recording
  7284-7287   resume_tracking
  4978-4983   run_archive_rules
 24644-24903  run_bot
 12265-12359  run_flask
  4953-4956   sample_bandwidth_for_active
  4379-4385   save_tiktok_check
  4646-4652   set_recording_file
  4485-4489   set_tracking_paused
  5204-5207   soft_delete_recording
  9246-9256   split_and_send_video
  5366-5408   start
  4304-4318   start_recording_attempt
  6490-6528   stats
  5143-5196   stop_manual_recording
  7290-7337   stoprec
  6714-6722   summary_cmd
  7441-7512   sysres
  5867-6011   teststream
  5410-5451   tiktok
  7106-7163   topusers
  5578-5635   track
  5543-5575   track_exact
  5649-5716   tracklist
  5027-5141   trigger_manual_recording
  4607-4644   try_acquire_recording_lock
  5220-5222   universal_search
 24573-24601  unpause_cmd
  5637-5647   untrack
 24400-24506  update_cmd
  4910-4913   update_recording_fingerprint
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
