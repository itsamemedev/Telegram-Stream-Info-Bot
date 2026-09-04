# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (71)

```
 10191  GET              /                                                dashboard
 12582  GET              /api/abo/status                                  api_abo_status
 10264  GET              /api/active-recordings                           api_active_recordings
 12653  GET              /api/activity-pulse                              api_activity_pulse
 12514  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11112  GET              /api/automation/status                           api_automation_status
 11134  POST             /api/automation/toggle                           api_automation_toggle
 12546  GET              /api/bandwidth/live                              api_bandwidth_live
 12499  GET              /api/bookmarks                                   api_bookmarks_list
 19363  GET              /api/channel/categories                          api_channel_categories
 19369  POST             /api/channel/set                                 api_channel_set
 19216  GET              /api/channels/status                             api_channels_status
 10245  GET              /api/checks                                      api_checks
 18890  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 18873  GET              /api/clips                                       api_clips
 18919  POST/DELETE      /api/clips/clear                                 api_clips_clear
 12925  GET              /api/community/stats                             api_community_stats
 19800  GET              /api/data/export                                 api_data_export
 18788  GET              /api/debug/threads                               api_debug_threads
 20647  GET              /api/defense/attacks                             api_defense_attacks
 20614  GET              /api/defense/crowdsec                            api_defense_crowdsec
 20632  GET              /api/defense/fail2ban                            api_defense_fail2ban
 20338  GET              /api/defense/overview                            api_defense_overview
 12528  GET              /api/events                                      api_events
 11956  GET              /api/events/stream                               api_events_stream
 12541  GET              /api/forecast/storage                            api_forecast_storage
 11150  GET              /api/freeai/status                               api_freeai_status
 11622  GET              /api/health                                      api_health
 12559  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 12555  GET              /api/heatmap/recordings                          api_heatmap_recordings
 18820  GET              /api/highlights                                  api_highlights
 18832  POST             /api/highlights/config                           api_highlights_config
 10125  POST             /api/login                                       dashboard_login_submit
 12910  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 12879  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11871  GET              /api/notify/status                               api_notify_status
 11882  POST             /api/notify/test                                 api_notify_test
 10329  GET              /api/outcomes                                    api_outcomes
 12636  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12613  GET              /api/proxy/trend                                 api_proxy_trend
 11488  GET              /api/public/stats                                api_public_stats
 10225  GET              /api/pulse                                       api_pulse
 12133  GET              /api/recording-attempts                          api_recording_attempts
 12484  GET              /api/search                                      api_search
 20385  GET              /api/selftest                                    api_selftest
 18626  GET              /api/shield/stats                                api_shield_stats
 10297  GET              /api/summary/preview                             api_summary_preview
 12198  GET              /api/system                                      api_system
 12958  GET              /api/system/check_timing                         api_check_timing
 13050  GET              /api/system/config_drift                         api_config_drift
 11687  GET              /api/system/config_snapshot                      api_system_config_snapshot
 11729  GET              /api/system/preflight                            api_system_preflight
 11855  GET              /api/system/preflight_history                    api_system_preflight_history
 12021  GET              /api/system/resilience                           api_system_resilience
 12519  GET              /api/tags                                        api_tags_list
 10259  GET              /api/top                                         api_top
 10439  GET              /api/trend-7d                                    api_trend_7d
 18939  GET              /api/tts/<fn>                                    api_tts_file
 19665  GET              /api/upload_window                               api_upload_window
 10343  GET              /api/userstats                                   api_userstats
 11536  GET              /api/version                                     api_version
 12171  GET              /archive/<int:eid>/download                      archive_download
 12228  GET              /download/<int:recording_id>                     download
 12111  GET              /health                                          health
 18757  GET              /healthz                                         healthz
 10116  GET              /login                                           dashboard_login_page
 10146  GET              /logout                                          dashboard_logout
 10153  GET              /manifest.webmanifest                            pwa_manifest
 19638  GET              /overlay                                         overlay_page
 10177  GET              /pwa-icon-<variant>.png                          pwa_icon
 10163  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (288)

```
   185  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   155  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   994  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   734  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   865  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   845  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   883  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   807  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   347  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   358  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   368  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   391  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   398  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   409  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   542  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   640  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1232  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1264  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   331  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   947  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   927  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1100  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1148  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1199  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1058  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   902  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   366  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   630  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   512  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   495  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   487  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   323  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   339  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   674  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   639  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   659  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   546  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    40  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    69  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   216  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   241  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   246  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   154  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    90  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   213  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   111  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   333  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   319  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   341  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   165  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   397  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   388  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   305  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   181  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   222  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   234  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   363  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   272  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   258  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   370  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   277  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   208  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   174  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   157  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   184  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   121  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   106  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    83  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   144  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    70  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    72  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    44  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
    31  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    43  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    42  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    77  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   112  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   274  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   259  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   182  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    60  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    67  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   203  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   230  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   190  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   235  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   161  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   179  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   151  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    54  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   127  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    70  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   103  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   111  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    51  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   127  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   156  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   141  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    81  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   103  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   124  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
    71  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   171  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    35  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   191  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   211  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   238  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   211  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   210  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   232  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
    91  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   159  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   137  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    76  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   116  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   166  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   110  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   158  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   175  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   206  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   182  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   242  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   212  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    73  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   226  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
    69  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
    94  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   104  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    43  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    61  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   215  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
    91  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    57  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    68  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   133  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   128  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   119  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    44  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    83  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   258  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   325  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   353  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   204  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   271  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   506  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    71  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   169  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   152  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   392  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   168  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   451  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   426  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   823  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   905  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   933  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   944  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   810  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   872  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   859  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   840  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   485  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   480  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   528  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   411  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   738  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   502  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   465  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   438  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   712  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   582  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   671  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   577  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   510  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   290  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   755  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   378  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   633  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   788  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   773  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   334  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   572  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   558  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   541  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   598  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   691  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   587  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   477  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   455  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   496  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   513  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   565  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   431  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   256  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   156  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   587  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   404  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   125  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   526  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   552  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   182  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   207  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   379  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   134  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   144  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   315  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   305  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   340  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    56  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    77  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    43  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    93  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   118  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   209  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   204  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   264  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   439  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   331  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   361  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   117  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   264  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    79  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   289  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   221  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   245  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   176  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   141  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   201  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    47  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   228  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   443  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   472  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   392  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   405  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   501  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   378  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   253  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   298  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   322  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   309  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   155  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   267  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   125  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   359  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   414  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   112  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
    91  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   123  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   104  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   115  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    67  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
    91  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    45  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   454  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   420  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   479  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   459  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   442  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   435  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
    42  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    82  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   113  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    97  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   122  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   143  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   155  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    80  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   104  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    58  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   190  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
   373  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands (45)

```
 21113  /ai                     
 21572  /ask                    
 21204  /assign_role            
 21250  /ban                    
 21904  /botstats               
 21828  /clearwarns             
 21868  /clip                   
 21853  /clipoftheweek          
 21695  /clips                  
 21165  /create_category        
 21134  /create_channel         
 21193  /create_group           
 21176  /create_role            
 21150  /create_voice           
 21486  /daily                  
 21602  /event                  
 21645  /events                 
 21741  /follow                 
 21725  /help                   
 21239  /kick                   
 21468  /leaderboard            
 21681  /livenow                
 21711  /post_test              
 21542  /profile                
 21274  /purge                  
 21454  /rank                   
 21668  /recstatus              
 21215  /remove_role            
 21127  /restream_status        
 21226  /set_channel_perms      
 21419  /setup_community        
 21437  /setup_targets          
 21767  /stats                  
 21039  /status                 
 22063  /streaminfo             
 21960  /sys_report             
 21936  /sys_unpause            
 21261  /timeout                
 21839  /topstreamers           
 21069  /track                  
 21053  /tracklist              
 21756  /unfollow               
 21102  /untrack                
 21789  /warn                   
 21813  /warnings               
```

## Discord-Events (4)

```
 22549  on_member_join
 22511  on_message
 22150  on_raw_reaction_add
 22584  on_ready
```

## Top-Level-Symbole in bot.py (479 Funktionen, 2 Klassen)

```
  2513-2514   _abo_key
  2534-2552   _abo_probe_dump
 19907-19917  _active_recorder_sync
 15891-15898  _ad_allowlist
 17032-17038  _agent_for
 19919-19937  _ai_calls_total_sync
 17041-17057  _ai_telemetry
 17546-17564  _alert
 22700-22750  _alert_monitor_loop
 23102-23164  _announce_loop
  3455-3458   _anthropic_key
  3465-3467   _anthropic_model
  9869-9872   _arg_int
  2505-2510   _as_dict
 17700-17722  _audio_tap_cmd
 10037-10048  _auth_cookie
 10004-10033  _auth_guard
  1676-1681   _auto_on
 18592-18610  _auto_restream_loop
 24215-24230  _azrael_broadcast_reply
 24115-24137  _azrael_chat_reply
 24098-24112  _azrael_chat_should_reply
 24143-24145  _azrael_gate_cfg
 17062-17076  _azrael_live_state
 19550-19564  _azrael_overlay_state
 17428-17482  _azrael_proactive_loop
 16880-16936  _azrael_reaction_to_chats
 24148-24155  _azrael_reply_all_chats
 24085-24095  _azrael_self_names
 24183-24212  _azrael_send_to
 17082-17103  _azrael_system
 22834-22837  _backup_active
 22915-22928  _backup_loop
 22662-22671  _brain_growth_loop
 10490-10517  _brain_growth_snapshot
  2441-2461   _brain_hint_delay
  6302-6330   _brain_notify
 11935-11952  _browser_push
  6346-6433   _build_daily_summary
  2944-3124   _build_native_cmd
 14079-14266  _build_restream_cmd
  3168-3201   _build_ytdlp_cmd
 19859-19866  _cached_probe
  5124-5151   _can_stop_tracking
  1856-1878   _capture_set_cookies
 12694-12697  _cfg_get
 12700-12702  _cfg_set
 19324-19359  _channel_set_all
 13322-13325  _chat_connected
 13328-13344  _chat_disconnected
  8360-8371   _chat_is_forum
 13364-13366  _chat_sanitize
 13307-13319  _chat_stat
 13347-13350  _chat_stats_snapshot
  3733-3744   _check_ai_alive_sync
  3747-3759   _check_ai_models_sync
 19868-19881  _check_redis_alive_sync
 19883-19903  _check_redis_version_sync
 10785-10828  _classify_pool_anonymity
 10831-10848  _classify_pool_anonymity_bg
   824-828    _claude_chat_sync_metered
  9898-9905   _client_ip
 23196-23223  _clip_prune
 23226-23236  _clip_recfile_for
 23749-23755  _clip_should_velocity
 23277-23359  _clip_to_discord
  3631-3640   _close_ai_session
 24261-24276  _cohost_broadcast
 24246-24247  _cohost_cfg
 24302-24314  _cohost_fire_highlight
 24250-24258  _cohost_gate
 24279-24299  _cohost_highlight
 23408-23442  _community_events_loop
 10390-10392  _conv_messages
  6702-6745   _cookie_alarm_loop
  1928-1932   _cookie_autorefresh_info
  1833-1837   _cookie_header
 11985-12017  _cpu_load_snapshot
  3953-3965   _create_index_safe
 20140-20246  _crowdsec_status
 20086-20137  _crowdsec_via_lapi
 19951-19969  _cscli_bin
 19975-19988  _cscli_path
  6592-6617   _daily_summary_loop
 20006-20023  _darf_journal_lesen
 22674-22697  _db_maintenance_loop
  6561-6589   _db_vacuum_loop
 15914-15938  _detect_foreign_ad
  1414-1425   _diag_path_owner
 17334-17378  _director_finalize
 18146-18153  _director_for
 17283-17331  _director_mark
 23643-23678  _disc_automod_check
 23619-23622  _disc_state_get
 23625-23632  _disc_state_set
 20689-20702  _discord_guild_filesize_bytes
 20896-20900  _discord_invite
 23580-23616  _discord_live_thread
 17485-17497  _discord_notify
 20795-20820  _discord_ops_alert
 23478-23576  _discord_post_user
 20956-22659  _discord_run_once
 20835-20893  _discord_start
 23167-23173  _discord_stop
 20710-20712  _discord_upload_limit_label
 20705-20707  _discord_upload_limit_mb
  6620-6697   _disk_alarm_loop
 25694-25743  _disk_autoclean
 25746-25759  _disk_guard_loop
 25686-25691  _disk_pct
 13672-13674  _drawtext_chain
 12327-12329  _dump_all_threads
 10710-10774  _enrich_proxies_with_geo
  2073-2117   _ensure_cookie_file_netscape
 20903-20953  _ensure_discord_invite
 23373-23405  _ensure_error_channel
  8419-8422   _ensure_notify_topic
 10955-10992  _ensure_proxy_ready
  8373-8400   _ensure_topic
   681-683    _env_int
   686-688    _env_int_range
 23445-23475  _error_channel_loop
 17530-17543  _event_webhook
 13137-13150  _evolution_loop
  5744-5778   _extract_file_payload
  2189-2191   _extract_urls_from_streamurl_node
 19991-19998  _f2b_sudo_hint
 17566-17568  _faster_whisper_available
 10599-10617  _fetch_proxy_list
 17980-18008  _fetch_tiktok_room_id
   757-760    _ff_cmd
 13838-13843  _find_chromium
  3161-3165   _find_external_recorder
  2194-2196   _find_stream_urls
 12745-12770  _fire_webhooks
  7482-7491   _fork_safe
   839-848    _freeai_chat_sync_metered
 20041-20083  _geo_lookup_ips
  3619-3628   _get_ai_session
  7315-7355   _get_live_info
  2731-2738   _get_resolve_semaphore
  7715-8081   _handle_single_tracking
 25512-25514  _hb
 25517-25534  _hb_while
 13373-13375  _highlight_cfg
 13378-13407  _highlight_observe
 13846-13864  _htmlov_screenshot_cmd
 17724-17734  _httpx_proxy
 12778-12790  _in_quiet_hours
 26585-26616  _install_fast_eventloop
  9764-9818   _install_fast_json
 12332-12348  _install_faulthandler
 18665-18674  _intel_ensure_schema
 18712-18747  _intel_index_loop
 18686-18696  _intel_index_one
 18677-18683  _intel_semantic
  5113-5122   _is_authorized
  7616-7622   _is_dead
  2179-2181   _is_hevc
 20026-20032  _is_private_ip
  1578-1585   _is_process_running
  6332-6343   _is_quiet_hours
  1215-1224   _is_upload_window
  9853-9866   _json_error_handler
  6555-6556   _kick_broadcaster_id
  6467-6509   _kick_follower_count
  6451-6454   _kick_slug
 11563-11594  _kick_user_token
  4002-4005   _kind_from_filename
 12807-12812  _latest_popularity
 18361-18394  _live_react_loop
 18157-18350  _live_react_worker
 16939-16950  _live_transcript_push
 18352-18359  _live_users
 17381-17425  _living_title_loop
  1754-1827   _load_cookies_dict
 22840-22912  _local_backup_scan
  9835-9849   _log_5xx
 14274-14286  _looks_like_codec_err
 14269-14271  _looks_like_source_expired
  7532-7562   _loop_fehler
 12352-12361  _loop_heartbeat
 25482-25509  _loop_lag_monitor
 12364-12432  _loop_watchdog_thread
 16819-16833  _loyalty_add
 16810-16816  _loyalty_get
 16836-16844  _loyalty_top
 12944-12946  _manual_donations_total
  7624-7625   _mark_dead
 11241-11257  _marketing_loop
 24162-24180  _maybe_handle_command
 25845-25869  _maybe_hype_clip
  3920-3943   _migrate_columns
 24441-24452  _mod_is_exempt
 24455-24460  _mod_warn_first
 24463-24466  _mod_warn_text
 13177-13185  _modlog
   966-968    _multistream_targets
  7494-7495   _nc_create_subprocess_exec
  7498-7499   _nc_create_subprocess_shell
 11493-11510  _news_loop
 13204-13206  _normalize_ingest
  2372-2389   _note_check_duration
  8413-8416   _notify_topic_name
 16965-16973  _oracle_memories
 17238-17272  _oracle_memorize
 16976-16989  _oracle_persona
 16958-16962  _oracle_recent_text
 13498-13506  _ov_atomic_write
 13486-13492  _ov_bar
 15817-15829  _ov_clip_text
 13495-13496  _ov_oneline
 19602-19631  _overlay_push
 13792-13835  _overlay_render_size
 13270-13274  _overlay_session_reset
 19566-19569  _overlay_src_ok
 15901-15911  _own_invites
 13787-13789  _parse_size
 20254-20334  _parse_ssh_attacks
  6917-6950   _pause_resume_cmd
  1882-1926   _persist_refreshed_cookies
  1720-1752   _pick_checked_pull_proxy
  9934-9947   _pin_auth_value
  9993-9994   _pin_clear_fail
  9973-9976   _pin_locked
  9979-9990   _pin_note_fail
  9950-9970   _pin_ok
 19460-19485  _piper_pick_model
 19497-19544  _piper_say
 12707-12742  _post_json_threaded
 13766-13784  _probe_video_size
  1606-1623   _proc_is_recorder
 10697-10708  _proxy_geo_cache_put
 10924-10952  _proxy_pool_refresh_loop
  1686-1717   _proxy_report_recording
 12317-12319  _prune_stall_dumps
 11311-11432  _public_stats
 17501-17527  _push_notify
 10095-10097  _pwa_dir
 10668-10683  _quick_validate_proxy
 12773-12775  _quiet_hours_config
 10060-10093  _rate_guard
 16784-16790  _react_warn
  7402-7441   _reap_proc
  2412-2434   _record_check_outcome
   752-754    _redact_stream_urls
 10851-10921  _refresh_proxy_pool
  2205-2295   _resolve_via_html
  2554-2708   _resolve_via_webcast_api_v2
  2771-2833   _resolve_via_ytdlp
 23789-23918  _resolve_youtube_ingest
 13253-13264  _restream_active_sources
 18011-18110  _restream_chat_guardian
 13410-13482  _restream_chat_push
 13867-13954  _restream_html_overlay_start
 13957-13970  _restream_html_overlay_stop
 13215-13238  _restream_overlay_files
 18398-18430  _restream_platform_state
 18554-18589  _restream_resume_after_restart
 14018-14076  _restream_tts_enqueue_wav
 13728-13760  _restream_tts_feeder
 13725-13726  _restream_tts_fifo_path
 13973-14000  _restream_tts_start
 14002-14016  _restream_tts_stop
 18436-18551  _restream_verify_loop
 22805-22817  _retention_loop
 22799-22802  _retention_scan
  2516-2518   _room_is_abo
  5782-5899   _run_ai_call
 12455-12468  _run_async_from_flask
 20035-20038  _run_priv
 26573-26581  _run_selfcheck_and_exit
 22820-22831  _s3_client
  7651-7702   _safe_send
  4624-4640   _sample_net_throughput
  2464-2491   _schedule_next_check
 22753-22796  _scheduler_loop
  3946-3950   _schema_pk
 12472-12477  _scraper_session
 24469-24508  _screen_full
 11638-11675  _sec_headers
  2184-2186   _select_stream_from_data_section
 26386-26570  _selfcheck
  8425-8459   _send_live_notice
  1238-1242   _should_defer_upload
 23239-23274  _shrink_for_discord
 10100-10112  _sicheres_ziel
 25766-25783  _sign_health_check
 25786-25805  _sign_health_loop
  7511-7522   _spawn
 26845-26875  _spawn_from_flask
 20378-20381  _st_befund
 17736-17977  _start_chat_listener
 12435-12452  _start_loop_watchdog
 11456-11484  _stats_loop
 11435-11438  _stats_output_path
 11441-11453  _stats_write
  8153-8169   _storage_cleanup_loop
 25825-25832  _story_for
  3223-3229   _stream_url_expiry
  3238-3244   _stream_url_is_fresh
  3231-3236   _stream_url_ttl
 15864-15871  _streamer_persona_get
 13677-13681  _studio_chain
 22937-23059  _system_backup
 23068-23098  _system_backup_loop
 10620-10659  _test_proxy
 11189-11205  _testpush_resolve_live
  7627-7648   _tg_sprache_setzen
  8332-8342   _tg_topics_load_into_mem
  8329-8330   _tg_topics_path
  8344-8351   _tg_topics_save
  9908-9916   _token_ok
  8354-8358   _topic_forget
 12793-12804  _tracking_max_duration
  4211-4225   _tracking_remove_cleanup
  4242-4254   _tracking_resume_cleanup
  1472-1495   _try_attach_file_handler
 19487-19495  _tts_cleanup
 11165-11169  _tunnel_effective
 18983-19036  _twitch_channel_status
 24511-24656  _twitch_chat_loop
 24325-24428  _twitch_eventsub_loop
  1261-1274   _upload_queue_add
  1285-1287   _upload_queue_count
  1244-1253   _upload_queue_load
  1234-1236   _upload_queue_path
  1276-1283   _upload_queue_remove
  1255-1259   _upload_queue_save
  1289-1330   _upload_window_loop
  7375-7382   _uptime_s
 13192-13201  _url_host
   732-749    _url_ohne_zugang
   817-821    _usage_record_claude
  7565-7609   _verbindung_verloren
  6512-6543   _viewer_sample_loop
  9997-10000  _wants_html
  7385-7399   _warn_empty_env
 25555-25676  _watchdog_loop
 24064-24072  _wchat_thank_ok
 17570-17600  _whisper_get_model
  7472-7479   _whisper_native_section
 16771-16777  _whisper_pool
 17669-17698  _whisper_segments
 17602-17666  _whisper_transcribe
 13508-13670  _write_restream_overlay
 24680-24760  _youtube_api_chat_loop
 19039-19142  _youtube_api_status
 19145-19212  _youtube_channel_status
 24763-24924  _youtube_chat_loop
 23924-23937  _youtube_restream_autoconfig
 23940-23964  _youtube_restream_autoconfig_inner
 24031-24059  _youtube_send
 19280-19321  _youtube_set_channel
 23967-24001  _yt_access_token
 24004-24019  _yt_live_chat_id
 24027-24028  _yt_sendrate_cfg
 24659-24674  _yt_timeout
  2755-2756   _ytdlp_detect_available
  2758-2769   _ytdlp_note_result
 12322-12324  _zombie_child_count
  7251-7275   about
  4121-4125   add_ai_log_entry
  4038-4041   add_archive_entry
  4701-4703   add_archive_rule
  4413-4447   add_recording
  4186-4203   add_tracking
  5902-5935   ai
  3773-3824   ai_chat
  3858-3868   ai_history_append
  3870-3875   ai_history_clear
  3847-3856   ai_history_load
  3832-3845   ai_rate_limit_check
  5964-5972   aireset
 17106-17125  azrael_chat
 24929-25051  brain_cmd
  3247-3431   build_recording_cmd
  4206-4209   bulk_add_trackings
  6748-6807   bulkadd
  8172-8312   check_all_trackings
  4258-4270   claim_live_transition
 15941-16703  class KickModerator
 14289-15704  class RestreamManager
 11038-11080  classify_proxy_anonymity
  6010-6208   cleanup
  5008-5014   cleanup_old_recordings
  4404-4411   clear_recording
 23681-23746  clip_moment
  4568-4617   compute_storage_forecast
  6870-6914   cookies_cmd
  4177-4183   count_trackings_for_chat
  4108-4119   decide_preferred_recorder
  4048-4051   delete_archive_entry
  4705-4707   delete_archive_rule
  5439-5586   diag
 25163-25224  einnahmen_cmd
  4562-4565   find_recordings_by_fingerprint
  4069-4085   finish_recording_attempt
  4230-4232   get_all_active_trackings
  4136-4139   get_all_checks
  4449-4452   get_all_recordings
  4511-4513   get_all_tags_with_counts
  4539-4542   get_annotations_for_recording
  4043-4046   get_archive_entry
  4532-4535   get_bookmarked_recordings
  1949-2066   get_cookie_health
  4499-4505   get_event_log
  4092-4106   get_last_recording_attempt
  2836-2941   get_live_status
  4890-4893   get_manual_recordings
  4547-4550   get_or_compute_inspect_sync
  5049-5093   get_outcome_breakdown
  4518-4521   get_priority_poll_interval
  4087-4090   get_recent_recording_attempts
  4454-4457   get_recording_by_id
  4525-4528   get_recording_note
  3565-3588   get_redis
  4166-4169   get_stats
  5002-5006   get_storage_stats
  4725-4727   get_tiktok_status_distribution
  4272-4281   get_tracking_state
  4227-4228   get_trackings_for_group
  4906-4909   get_trash_recordings
  9080-9743   handle_recording_finished
  3968-3993   init_db
  4697-4699   list_archive_rules
  5243-5281   live
  7705-7713   live_check_worker
  3643-3677   llm_chat
  3700-3728   llm_chat_sync
  3685-3697   llm_list_models
  4465-4491   log_event
  1540-1573   log_recording_failure
  7064-7113   logs_cmd
 25873-26376  main
  5938-5961   on_ai_media
  7190-7216   on_ai_reply
  7219-7248   on_azrael_mention
  7280-7310   on_callback
 17131-17235  oracle_handle
  6953-6956   pause_tracking
  5103-5108   profile_keyboard
  7015-7061   quota
  8083-8150   reaper_loop
  4721-4723   record_tiktok_status
  5977-6007   recstatus
  3590-3598   redis_get_json
  3601-3607   redis_set_json
 25227-25237  report_cmd
 11083-11085  report_proxy_result
  2298-2325   resolve_tiktok_live_stream
  4901-4904   restore_recording
  6959-6962   resume_tracking
  4710-4715   run_archive_rules
 25240-25462  run_bot
 12242-12289  run_flask
  4643-4688   sample_bandwidth_for_active
  4128-4134   save_tiktok_check
  4396-4402   set_recording_file
  4235-4239   set_tracking_paused
  4896-4899   soft_delete_recording
  8465-9078   split_and_send_video
  5156-5198   start
  4053-4067   start_recording_attempt
  6211-6249   stats
  4871-4888   stop_manual_recording
  6965-7012   stoprec
  6436-6444   summary_cmd
  7116-7187   sysres
  5588-5732   teststream
  5200-5241   tiktok
  6810-6867   topusers
  5318-5375   track
  5283-5315   track_exact
  5389-5437   tracklist
  4737-4869   trigger_manual_recording
  4357-4394   try_acquire_recording_lock
  4912-4971   universal_search
  5377-5387   untrack
 25054-25160  update_cmd
  4557-4560   update_recording_fingerprint
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
binresolve.py          resolve
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
highlights.py          check, new_state, observe, score
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             broadcaster_id, configure, oauth_exchange, slug
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             changelog, current, latest, summary_line
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
