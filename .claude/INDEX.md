# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
  9963  GET              /                                                dashboard
 11855  GET              /api/abo/status                                  api_abo_status
 11809  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10751  GET              /api/automation/status                           api_automation_status
 10773  POST             /api/automation/toggle                           api_automation_toggle
 18358  GET              /api/channel/categories                          api_channel_categories
 18364  POST             /api/channel/set                                 api_channel_set
 18211  GET              /api/channels/status                             api_channels_status
 17885  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 17868  GET              /api/clips                                       api_clips
 17914  POST/DELETE      /api/clips/clear                                 api_clips_clear
 17793  GET              /api/debug/threads                               api_debug_threads
 11820  GET              /api/events                                      api_events
 11392  GET              /api/events/stream                               api_events_stream
 11219  GET              /api/health                                      api_health
 17827  POST             /api/highlights/config                           api_highlights_config
  9897  POST             /api/login                                       dashboard_login_submit
 12148  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11307  GET              /api/notify/status                               api_notify_status
 11318  POST             /api/notify/test                                 api_notify_test
 11909  GET              /api/proxy/heatmap                               api_proxy_heatmap
 11886  GET              /api/proxy/trend                                 api_proxy_trend
 17934  GET              /api/tts/<fn>                                    api_tts_file
 18660  GET              /api/upload_window                               api_upload_window
 11509  GET              /archive/<int:eid>/download                      archive_download
 11537  GET              /download/<int:recording_id>                     download
 11466  GET              /health                                          health
 17762  GET              /healthz                                         healthz
  9888  GET              /login                                           dashboard_login_page
  9918  GET              /logout                                          dashboard_logout
  9925  GET              /manifest.webmanifest                            pwa_manifest
 18633  GET              /overlay                                         overlay_page
  9949  GET              /pwa-icon-<variant>.png                          pwa_icon
  9935  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (327)

```
   182  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   394  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
  1003  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   743  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   874  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   854  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   892  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   816  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   551  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   649  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1241  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1273  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   340  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   956  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   936  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1109  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1157  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1208  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1067  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   911  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   389  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   653  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   535  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   518  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   510  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   346  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   362  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   697  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   662  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   682  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   569  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   216  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   241  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   246  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
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
   286  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   208  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   174  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   157  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   371  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   348  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   161  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   415  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   329  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   314  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   237  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   193  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    71  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    78  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   469  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   258  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   285  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   245  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
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
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   200  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   220  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   247  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   366  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   284  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   386  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   381  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   457  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
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
   400  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
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
   267  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   334  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   362  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   213  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   280  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   515  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   178  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   161  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   401  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   225  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   177  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   460  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   435  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   296  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   142  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   832  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   914  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   942  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   953  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   819  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   881  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   868  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   849  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   319  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   494  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   489  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   537  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   420  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   747  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   511  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   474  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   447  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   721  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   591  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   680  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   586  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   519  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   299  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   764  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   387  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   642  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   797  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   782  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   343  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   581  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   567  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   550  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   607  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   700  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   596  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   486  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   464  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   505  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   522  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   574  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   440  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   596  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   535  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   561  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   134  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   144  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   370  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   360  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   395  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   338  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   428  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   448  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   340  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   370  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
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
   206  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    72  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   117  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   140  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   104  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   370  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   361  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   176  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   238  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   453  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   482  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   402  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   415  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   511  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   388  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   263  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   308  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   332  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   319  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   165  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   277  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   135  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   369  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   424  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   252  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   463  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   429  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   488  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   468  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   451  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   444  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   238  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   305  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
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
   382  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands (45)

```
 19653  /ai                     
 20126  /ask                    
 19744  /assign_role            
 19790  /ban                    
 20458  /botstats               
 20382  /clearwarns             
 20422  /clip                   
 20407  /clipoftheweek          
 20249  /clips                  
 19705  /create_category        
 19674  /create_channel         
 19733  /create_group           
 19716  /create_role            
 19690  /create_voice           
 20026  /daily                  
 20156  /event                  
 20199  /events                 
 20295  /follow                 
 20279  /help                   
 19779  /kick                   
 20008  /leaderboard            
 20235  /livenow                
 20265  /post_test              
 20096  /profile                
 19814  /purge                  
 19994  /rank                   
 20222  /recstatus              
 19755  /remove_role            
 19667  /restream_status        
 19766  /set_channel_perms      
 19959  /setup_community        
 19977  /setup_targets          
 20321  /stats                  
 19579  /status                 
 20617  /streaminfo             
 20514  /sys_report             
 20490  /sys_unpause            
 19801  /timeout                
 20393  /topstreamers           
 19609  /track                  
 19593  /tracklist              
 20310  /unfollow               
 19642  /untrack                
 20343  /warn                   
 20367  /warnings               
```

## Discord-Events (4)

```
 21115  on_member_join
 21077  on_message
 20704  on_raw_reaction_add
 21150  on_ready
```

## Top-Level-Symbole in bot.py (471 Funktionen, 2 Klassen)

```
  2614-2615   _abo_key
  2635-2653   _abo_probe_dump
 15125-15132  _ad_allowlist
 16064-16070  _agent_for
 16073-16089  _ai_telemetry
 16578-16596  _alert
 21289-21339  _alert_monitor_loop
 21691-21753  _announce_loop
  3556-3559   _anthropic_key
  3566-3568   _anthropic_model
  9641-9644   _arg_int
  2606-2611   _as_dict
 16731-16753  _audio_tap_cmd
  9809-9820   _auth_cookie
  9776-9805   _auth_guard
  1728-1733   _auto_on
 17624-17642  _auto_restream_loop
 22832-22847  _azrael_broadcast_reply
 22732-22754  _azrael_chat_reply
 22715-22729  _azrael_chat_should_reply
 22760-22762  _azrael_gate_cfg
 16094-16108  _azrael_live_state
 18545-18559  _azrael_overlay_state
 16460-16514  _azrael_proactive_loop
 15912-15968  _azrael_reaction_to_chats
 22765-22772  _azrael_reply_all_chats
 22702-22712  _azrael_self_names
 22800-22829  _azrael_send_to
 16114-16135  _azrael_system
 21423-21426  _backup_active
 21504-21517  _backup_loop
 21228-21237  _brain_growth_loop
 10142-10169  _brain_growth_snapshot
  2542-2562   _brain_hint_delay
  6234-6262   _brain_notify
 11371-11388  _browser_push
  6278-6365   _build_daily_summary
  3045-3225   _build_native_cmd
 13344-13531  _build_restream_cmd
  3269-3302   _build_ytdlp_cmd
  5056-5083   _can_stop_tracking
  1841-1863   _capture_set_cookies
 11963-11966  _cfg_get
 11969-11971  _cfg_set
 18319-18354  _channel_set_all
 12502-12505  _chat_connected
 12508-12524  _chat_disconnected
  8360-8371   _chat_is_forum
 12544-12546  _chat_sanitize
 12487-12499  _chat_stat
 12527-12530  _chat_stats_snapshot
  3839-3851   _check_ai_models_sync
 10424-10467  _classify_pool_anonymity
 10470-10487  _classify_pool_anonymity_bg
   828-850    _claude_chat_sync_metered
  9670-9677   _client_ip
 21785-21812  _clip_prune
 21815-21825  _clip_recfile_for
 22366-22372  _clip_should_velocity
 21866-21948  _clip_to_discord
  3732-3741   _close_ai_session
 22878-22893  _cohost_broadcast
 22863-22864  _cohost_cfg
 22919-22931  _cohost_fire_highlight
 22867-22875  _cohost_gate
 22896-22916  _cohost_highlight
 21997-22059  _community_events_loop
 10072-10074  _conv_messages
  6637-6698   _cookie_alarm_loop
  1932-1937   _cookie_autofetch_info
  1915-1919   _cookie_autorefresh_info
  1818-1822   _cookie_header
  1949-1982   _cookies_selbst_holen
  4045-4057   _create_index_safe
 18992-19098  _crowdsec_status
 18938-18989  _crowdsec_via_lapi
 18842-18860  _cscli_bin
 18869-18882  _cscli_path
  6527-6552   _daily_summary_loop
 18900-18917  _darf_journal_lesen
 21263-21286  _db_maintenance_loop
  6496-6524   _db_vacuum_loop
 15148-15172  _detect_foreign_ad
  1463-1474   _diag_path_owner
 16366-16410  _director_finalize
 17177-17184  _director_for
 16315-16363  _director_mark
 22260-22295  _disc_automod_check
 22236-22239  _disc_state_get
 22242-22249  _disc_state_set
 19436-19440  _discord_invite
 22197-22233  _discord_live_thread
 16517-16529  _discord_notify
 19335-19360  _discord_ops_alert
 22095-22193  _discord_post_user
 19496-21225  _discord_run_once
 19375-19433  _discord_start
 21756-21762  _discord_stop
  6555-6632   _disk_alarm_loop
 24308-24357  _disk_autoclean
 24360-24373  _disk_guard_loop
 12937-12939  _drawtext_chain
 11641-11643  _dump_all_threads
 10350-10413  _enrich_proxies_with_geo
  2157-2218   _ensure_cookie_file_netscape
 19443-19493  _ensure_discord_invite
 21962-21994  _ensure_error_channel
  8419-8422   _ensure_notify_topic
 10594-10631  _ensure_proxy_ready
  8373-8400   _ensure_topic
   688-690    _env_int
   693-695    _env_int_range
 22062-22092  _error_channel_loop
 16562-16575  _event_webhook
 12317-12330  _evolution_loop
  5676-5710   _extract_file_payload
  2290-2292   _extract_urls_from_streamurl_node
 18885-18892  _f2b_sudo_hint
  4556-4566   _fehler_text
 10251-10269  _fetch_proxy_list
 17011-17039  _fetch_tiktok_room_id
   761-764    _ff_cmd
 13103-13108  _find_chromium
  3262-3266   _find_external_recorder
  2295-2297   _find_stream_urls
 12014-12039  _fire_webhooks
  7464-7473   _fork_safe
   861-874    _freeai_chat_sync_metered
 18931-18935  _geo_lookup_ips
  3720-3729   _get_ai_session
  7297-7337   _get_live_info
  2832-2839   _get_resolve_semaphore
  7697-8074   _handle_single_tracking
 24130-24132  _hb
 24135-24152  _hb_while
 12558-12560  _highlight_cfg
 12563-12592  _highlight_observe
 13111-13129  _htmlov_screenshot_cmd
 16755-16765  _httpx_proxy
 12047-12059  _in_quiet_hours
 25199-25230  _install_fast_eventloop
  9536-9590   _install_fast_json
 11646-11662  _install_faulthandler
 17670-17679  _intel_ensure_schema
 17717-17752  _intel_index_loop
 17691-17701  _intel_index_one
 17682-17688  _intel_semantic
  5045-5054   _is_authorized
  7598-7604   _is_dead
  2280-2282   _is_hevc
 18920-18922  _is_private_ip
  1627-1634   _is_process_running
  6264-6275   _is_quiet_hours
  1256-1265   _is_upload_window
  9625-9638   _json_error_handler
  6490-6491   _kick_broadcaster_id
  6402-6444   _kick_follower_count
  6386-6389   _kick_slug
 11184-11191  _kick_user_token
  4094-4097   _kind_from_filename
 12076-12081  _latest_popularity
 17392-17425  _live_react_loop
 17188-17381  _live_react_worker
 15971-15982  _live_transcript_push
 17383-17390  _live_users
 16413-16457  _living_title_loop
 21429-21501  _local_backup_scan
  9607-9621   _log_5xx
 13539-13551  _looks_like_codec_err
 13534-13536  _looks_like_source_expired
  7514-7544   _loop_fehler
 11666-11675  _loop_heartbeat
 24100-24127  _loop_lag_monitor
 11678-11746  _loop_watchdog_thread
 15851-15865  _loyalty_add
 15842-15848  _loyalty_get
 15868-15876  _loyalty_top
 12189-12191  _manual_donations_total
  4763-4782   _manual_status
  7606-7607   _mark_dead
 10870-10886  _marketing_loop
 22779-22797  _maybe_handle_command
 24459-24483  _maybe_hype_clip
  4012-4035   _migrate_columns
 23058-23069  _mod_is_exempt
 23072-23077  _mod_warn_first
 23080-23083  _mod_warn_text
 12357-12365  _modlog
  1003-1005   _multistream_targets
  7476-7477   _nc_create_subprocess_exec
  7480-7481   _nc_create_subprocess_shell
 11121-11138  _news_loop
 12384-12386  _normalize_ingest
  2473-2490   _note_check_duration
  8413-8416   _notify_topic_name
 15997-16005  _oracle_memories
 16270-16304  _oracle_memorize
 16008-16021  _oracle_persona
 15990-15994  _oracle_recent_text
 12718-12726  _ov_atomic_write
 12706-12712  _ov_bar
 15051-15063  _ov_clip_text
 12715-12716  _ov_oneline
 18597-18626  _overlay_push
 13057-13100  _overlay_render_size
 12450-12454  _overlay_session_reset
 18561-18564  _overlay_src_ok
 15135-15145  _own_invites
 13052-13054  _parse_size
 19106-19186  _parse_ssh_attacks
  6899-6932   _pause_resume_cmd
  1869-1913   _persist_refreshed_cookies
  1772-1804   _pick_checked_pull_proxy
  9706-9719   _pin_auth_value
  9765-9766   _pin_clear_fail
  9745-9748   _pin_locked
  9751-9762   _pin_note_fail
  9722-9742   _pin_ok
 18455-18480  _piper_pick_model
 18492-18539  _piper_say
 11976-12011  _post_json_threaded
 13031-13049  _probe_video_size
  1655-1672   _proc_is_recorder
 10563-10591  _proxy_pool_refresh_loop
  1738-1769   _proxy_report_recording
 11631-11633  _prune_stall_dumps
 10940-11061  _public_stats
  1940-1946   _pull_proxy_still
 16533-16559  _push_notify
  9867-9869   _pwa_dir
 10320-10335  _quick_validate_proxy
 12042-12044  _quiet_hours_config
  9832-9865   _rate_guard
 15816-15822  _react_warn
  7384-7423   _reap_proc
  2513-2535   _record_check_outcome
   756-758    _redact_stream_urls
 10490-10560  _refresh_proxy_pool
  2306-2396   _resolve_via_html
  2655-2809   _resolve_via_webcast_api_v2
  2872-2934   _resolve_via_ytdlp
 22406-22535  _resolve_youtube_ingest
 12433-12444  _restream_active_sources
 17042-17141  _restream_chat_guardian
 12595-12667  _restream_chat_push
 12692-12701  _restream_chat_push_async
 13132-13219  _restream_html_overlay_start
 13222-13235  _restream_html_overlay_stop
 12395-12418  _restream_overlay_files
 17429-17461  _restream_platform_state
 17586-17621  _restream_resume_after_restart
 13283-13341  _restream_tts_enqueue_wav
 12993-13025  _restream_tts_feeder
 12990-12991  _restream_tts_fifo_path
 13238-13265  _restream_tts_start
 13267-13281  _restream_tts_stop
 17467-17583  _restream_verify_loop
 21394-21406  _retention_loop
 21388-21391  _retention_scan
  2617-2619   _room_is_abo
  5714-5831   _run_ai_call
 11769-11782  _run_async_from_flask
 18925-18928  _run_priv
 25187-25195  _run_selfcheck_and_exit
 21409-21420  _s3_client
  7633-7684   _safe_send
  4689-4705   _sample_net_throughput
  2565-2592   _schedule_next_check
 21342-21385  _scheduler_loop
  4038-4042   _schema_pk
 11786-11791  _scraper_session
 23086-23125  _screen_full
 11235-11272  _sec_headers
  2285-2287   _select_stream_from_data_section
 25000-25184  _selfcheck
  8425-8459   _send_live_notice
  1279-1283   _should_defer_upload
 21828-21863  _shrink_for_discord
  9872-9884   _sicheres_ziel
 21240-21260  _sicherheits_erinnerung_loop
 24380-24397  _sign_health_check
 24400-24419  _sign_health_loop
  7493-7504   _spawn
 25572-25602  _spawn_from_flask
 16767-17008  _start_chat_listener
 11749-11766  _start_loop_watchdog
 11088-11116  _stats_loop
 11067-11070  _stats_output_path
 11073-11085  _stats_write
  8153-8169   _storage_cleanup_loop
 24439-24446  _story_for
  3324-3330   _stream_url_expiry
  3339-3345   _stream_url_is_fresh
  3332-3337   _stream_url_ttl
 15098-15105  _streamer_persona_get
 12942-12946  _studio_chain
 21526-21648  _system_backup
 21657-21687  _system_backup_loop
 10272-10311  _test_proxy
 10818-10834  _testpush_resolve_live
  7609-7630   _tg_sprache_setzen
  8332-8342   _tg_topics_load_into_mem
  8329-8330   _tg_topics_path
  8344-8351   _tg_topics_save
  9680-9688   _token_ok
  8354-8358   _topic_forget
 12062-12073  _tracking_max_duration
  4302-4316   _tracking_remove_cleanup
  4333-4345   _tracking_resume_cleanup
  1521-1544   _try_attach_file_handler
 18482-18490  _tts_cleanup
 10794-10798  _tunnel_effective
 17978-18031  _twitch_channel_status
 23128-23273  _twitch_chat_loop
 22942-23045  _twitch_eventsub_loop
  1302-1315   _upload_queue_add
  1326-1328   _upload_queue_count
  1285-1294   _upload_queue_load
  1275-1277   _upload_queue_path
  1317-1324   _upload_queue_remove
  1296-1300   _upload_queue_save
  1330-1371   _upload_window_loop
  7357-7364   _uptime_s
 12372-12381  _url_host
   821-825    _usage_record_claude
  7547-7591   _verbindung_verloren
  6447-6478   _viewer_sample_loop
  9769-9772   _wants_html
  7367-7381   _warn_empty_env
 24173-24294  _watchdog_loop
 22681-22689  _wchat_thank_ok
 16601-16631  _whisper_get_model
  7454-7461   _whisper_native_section
 15803-15809  _whisper_pool
 16700-16729  _whisper_segments
 16633-16697  _whisper_transcribe
 12773-12935  _write_restream_overlay
 12735-12770  _write_restream_overlay_async
 23297-23377  _youtube_api_chat_loop
 18034-18137  _youtube_api_status
 18140-18207  _youtube_channel_status
 23380-23541  _youtube_chat_loop
 22541-22554  _youtube_restream_autoconfig
 22557-22581  _youtube_restream_autoconfig_inner
 22648-22676  _youtube_send
 18275-18316  _youtube_set_channel
 22584-22618  _yt_access_token
 22621-22636  _yt_live_chat_id
 22644-22645  _yt_sendrate_cfg
 23276-23291  _yt_timeout
  2856-2857   _ytdlp_detect_available
  2859-2870   _ytdlp_note_result
 11636-11638  _zombie_child_count
  7233-7257   about
  4213-4217   add_ai_log_entry
  4130-4133   add_archive_entry
  4727-4729   add_archive_rule
  4504-4538   add_recording
  4277-4294   add_tracking
  5834-5867   ai
  3865-3916   ai_chat
  3950-3960   ai_history_append
  3962-3967   ai_history_clear
  3939-3948   ai_history_load
  3924-3937   ai_rate_limit_check
  5896-5904   aireset
 16138-16157  azrael_chat
 23546-23668  brain_cmd
  3348-3532   build_recording_cmd
  4297-4300   bulk_add_trackings
  6701-6760   bulkadd
  8172-8312   check_all_trackings
  4349-4361   claim_live_transition
 15175-15735  class KickModerator
 13554-14938  class RestreamManager
 10677-10719  classify_proxy_anonymity
  5942-6140   cleanup
  4981-4987   cleanup_old_recordings
  4495-4502   clear_recording
 22298-22363  clip_moment
  4679-4682   compute_storage_forecast
  6823-6896   cookies_cmd
  4268-4274   count_trackings_for_chat
  4200-4211   decide_preferred_recorder
  4140-4143   delete_archive_entry
  4731-4733   delete_archive_rule
  5371-5518   diag
 23780-23841  einnahmen_cmd
  4673-4676   find_recordings_by_fingerprint
  4161-4177   finish_recording_attempt
  4321-4323   get_all_active_trackings
  4228-4230   get_all_checks
  4540-4543   get_all_recordings
  4622-4624   get_all_tags_with_counts
  4650-4653   get_annotations_for_recording
  4135-4138   get_archive_entry
  4643-4646   get_bookmarked_recordings
  2004-2150   get_cookie_health
  4610-4616   get_event_log
  4184-4198   get_last_recording_attempt
  2937-3042   get_live_status
  4920-4923   get_manual_recordings
  4658-4661   get_or_compute_inspect_sync
  5022-5025   get_outcome_breakdown
  4629-4632   get_priority_poll_interval
  4179-4182   get_recent_recording_attempts
  4545-4548   get_recording_by_id
  4636-4639   get_recording_note
  3666-3689   get_redis
  4257-4260   get_stats
  4975-4979   get_storage_stats
  4751-4753   get_tiktok_status_distribution
  4363-4372   get_tracking_state
  4318-4319   get_trackings_for_group
  4936-4939   get_trash_recordings
  8847-9515   handle_recording_finished
  4060-4085   init_db
  4723-4725   list_archive_rules
  5175-5213   live
  7687-7695   live_check_worker
  3744-3778   llm_chat
  3801-3829   llm_chat_sync
  3786-3798   llm_list_models
  4569-4602   log_event
  1589-1622   log_recording_failure
  7046-7095   logs_cmd
 24487-24990  main
  5870-5893   on_ai_media
  7172-7198   on_ai_reply
  7201-7230   on_azrael_mention
  7262-7292   on_callback
 16163-16267  oracle_handle
  6935-6938   pause_tracking
  5035-5040   profile_keyboard
  6997-7043   quota
  8076-8150   reaper_loop
  4747-4749   record_tiktok_status
  5909-5939   recstatus
  3691-3699   redis_get_json
  3702-3708   redis_set_json
 23844-23854  report_cmd
 10722-10724  report_proxy_result
  2399-2426   resolve_tiktok_live_stream
  4931-4934   restore_recording
  6941-6944   resume_tracking
  4736-4741   run_archive_rules
 23857-24080  run_bot
 11551-11603  run_flask
  4711-4714   sample_bandwidth_for_active
  4220-4226   save_tiktok_check
  4487-4493   set_recording_file
  4326-4330   set_tracking_paused
  4926-4929   soft_delete_recording
  8465-8845   split_and_send_video
  5088-5130   start
  4145-4159   start_recording_attempt
  6143-6181   stats
  4901-4918   stop_manual_recording
  6947-6994   stoprec
  6371-6379   summary_cmd
  7098-7169   sysres
  5520-5664   teststream
  5132-5173   tiktok
  6763-6820   topusers
  5250-5307   track
  5215-5247   track_exact
  5321-5369   tracklist
  4785-4899   trigger_manual_recording
  4448-4485   try_acquire_recording_lock
  4942-4944   universal_search
  5309-5319   untrack
 23671-23777  update_cmd
  4668-4671   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
binresolve.py          resolve
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookieholen.py         aktualisiere, aus_browser, configure, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            geschuetzt, host, lage, nur_lokal, offen_im_netz
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_async, db_conn, get_pool, set_pool
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, configure, oauth_exchange, search_category, send_message, slug, timeout_user, update_channel, user_token
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls, url_ohne_zugang
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
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
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
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
